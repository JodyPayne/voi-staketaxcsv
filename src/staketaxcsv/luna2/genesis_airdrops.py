import logging

import staketaxcsv.common.ibc.api_lcd_v1
import staketaxcsv.luna2.constants as co
from staketaxcsv.luna2.make_tx import make_genesis_airdrop1_tx, make_vesting_airdrop_tx
from staketaxcsv.settings_csv import LUNA2_NODE
from datetime import datetime, timedelta


def genesis_airdrops(wallet_address, exporter):
    # genesis airdrop
    _genesis_airdrop(wallet_address, exporter)

    # vesting airdrops
    _vesting_airdrops(wallet_address, exporter)


def _genesis_airdrop(wallet_address, exporter):
    amount_luna = _genesis_airdrop_luna_amount(wallet_address)
    if amount_luna:
        row = make_genesis_airdrop1_tx(amount_luna, wallet_address)
        exporter.ingest_row(row)


def _genesis_airdrop_luna_amount(wallet_address):
    data = staketaxcsv.common.ibc.api_lcd_v1.LcdAPI_v1(LUNA2_NODE).balances(wallet_address, height=1)
    balances_elem = data["balances"]

    if len(balances_elem) == 0:
        return 0

    denom = balances_elem[0]["denom"]
    amount_string = balances_elem[0]["amount"]
    assert (denom == "uluna")
    return float(amount_string) / co.MILLION


# https://docs.terra.money/develop/vesting
def _vesting_airdrops(wallet_address, exporter):
    data = staketaxcsv.common.ibc.api_lcd_v1.LcdAPI_v1(LUNA2_NODE).account(wallet_address)

    if data.get("account", {}).get("@type", "") == "/cosmos.vesting.v1beta1.PeriodicVestingAccount":
        account = data["account"]
        start_time = int(account["start_time"])
        vesting_periods = account["vesting_periods"]

        # Pre-calculate the start times for each vesting period
        period_start_times = [start_time]
        for period in vesting_periods:
            start_time += int(period["length"])
            period_start_times.append(start_time)

        # Main loop to create and ingest transactions
        for period, cur_time in zip(vesting_periods, period_start_times):
            length_seconds = int(period["length"])
            length_days = length_seconds // 86400
            amount = period["amount"]

            # Omit the first vesting period, as it has negligible amounts and indicates a cliff
            if length_seconds == 15552000:
                continue

            if len(amount) > 0:
                amount_luna = float(amount[0]["amount"]) / co.MILLION
                daily_amount_luna = amount_luna / length_days if length_days > 0 else 0

                for day in range(length_days):
                    # Calculate and format the timestamp for this day of the vesting period
                    timestamp_date = datetime.utcfromtimestamp(cur_time + day * 86400)
                    timestamp_str = timestamp_date.strftime("%Y-%m-%d %H:%M:%S")

                    # Check if the calculated timestamp is in the future
                    if timestamp_date > datetime.utcnow():
                        break  # Stop adding transactions for future dates

                    # Create and ingest the transaction row
                    row = make_vesting_airdrop_tx(daily_amount_luna, wallet_address, timestamp_str)
                    exporter.ingest_row(row)

    else:
        logging.info("No vesting airdrops found")
