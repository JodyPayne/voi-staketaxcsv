from staketaxcsv.common.Exporter import Row
from staketaxcsv.common.ExporterTypes import (
    TX_TYPE_AIRDROP,
    TX_TYPE_BORROW,
    TX_TYPE_DEPOSIT_COLLATERAL,
    TX_TYPE_EXCLUDED,
    TX_TYPE_INCOME,
    TX_TYPE_LP_DEPOSIT,
    TX_TYPE_LP_STAKE,
    TX_TYPE_LP_UNSTAKE,
    TX_TYPE_LP_WITHDRAW,
    TX_TYPE_REPAY,
    TX_TYPE_SOL_TRANSFER_SELF,
    TX_TYPE_SPEND,
    TX_TYPE_STAKE,
    TX_TYPE_STAKING,
    TX_TYPE_TRADE,
    TX_TYPE_TRANSFER,
    TX_TYPE_UNKNOWN,
    TX_TYPE_UNSTAKE,
    TX_TYPE_WITHDRAW_COLLATERAL,
)
from staketaxcsv.settings_csv import DONATION_WALLETS


def make_swap_tx(txinfo, sent_amount, sent_currency, received_amount, received_currency, txid=None, empty_fee=False, z_index=0):
    """
    Creates a transaction for a token swap.
    """
    return _make_tx_exchange(txinfo, sent_amount, sent_currency, received_amount, received_currency, TX_TYPE_TRADE, txid, empty_fee, z_index)


def make_income_tx(txinfo, income_amount, income_currency, txid=None, empty_fee=False, z_index=0):
    """
    Creates a transaction for earned income.
    """
    return _make_tx_received(txinfo, income_amount, income_currency, TX_TYPE_INCOME, txid, empty_fee=empty_fee, z_index=z_index)


def make_reward_tx(txinfo, reward_amount, reward_currency, txid=None, empty_fee=False, z_index=0):
    """
    Creates a transaction for staking rewards.
    """
    return _make_tx_received(txinfo, reward_amount, reward_currency, TX_TYPE_STAKING, txid, empty_fee=empty_fee, z_index=z_index)


def make_transfer_in_tx(txinfo, received_amount, received_currency, z_index=0):
    """
    Creates a transaction for a transfer received by the wallet.
    """
    txinfo.fee = ""
    txinfo.fee_currency = ""
    return _make_tx_received(txinfo, received_amount, received_currency, TX_TYPE_TRANSFER, z_index=z_index)


def make_transfer_out_tx(txinfo, sent_amount, sent_currency, dest_address=None, z_index=0):
    """
    Creates a transaction for a transfer sent from the wallet.
    """
    if dest_address and dest_address in DONATION_WALLETS:
        return make_spend_tx(txinfo, sent_amount, sent_currency, z_index)
    else:
        return _make_tx_sent(txinfo, sent_amount, sent_currency, TX_TYPE_TRANSFER, z_index=z_index)


def make_unknown_tx(txinfo, z_index=0, empty_fee=False):
    """
    Creates a transaction with an unknown type.
    """
    return make_simple_tx(txinfo, TX_TYPE_UNKNOWN, z_index, empty_fee)


def make_simple_tx(txinfo, tx_type, z_index=0, empty_fee=False):
    """
    Creates a basic transaction row with specified type.
    """
    fee = "" if empty_fee else txinfo.fee
    fee_currency = txinfo.fee_currency if fee else ""

    return Row(
        timestamp=txinfo.timestamp,
        tx_type=tx_type,
        received_amount="",
        received_currency="",
        sent_amount="",
        sent_currency="",
        fee=fee,
        fee_currency=fee_currency,
        exchange=txinfo.exchange,
        wallet_address=txinfo.wallet_address,
        txid=txinfo.txid,
        url=txinfo.url,
        z_index=z_index,
        comment=txinfo.comment,
    )


def _make_tx_received(txinfo, received_amount, received_currency, tx_type, txid=None, empty_fee=False, z_index=0):
    """
    Helper function to create a transaction where tokens are received.
    """
    txid = txid if txid else txinfo.txid
    fee = "" if empty_fee else txinfo.fee
    fee_currency = txinfo.fee_currency if fee else ""

    return Row(
        timestamp=txinfo.timestamp,
        tx_type=tx_type,
        received_amount=received_amount,
        received_currency=received_currency,
        sent_amount="",
        sent_currency="",
        fee=fee,
        fee_currency=fee_currency,
        exchange=txinfo.exchange,
        wallet_address=txinfo.wallet_address,
        txid=txid,
        url=txinfo.url,
        z_index=z_index,
        comment=txinfo.comment,
    )


def _make_tx_sent(txinfo, sent_amount, sent_currency, tx_type, empty_fee=False, z_index=0):
    """
    Helper function to create a transaction where tokens are sent.
    """
    fee = "" if empty_fee else txinfo.fee
    fee_currency = txinfo.fee_currency if fee else ""

    return Row(
        timestamp=txinfo.timestamp,
        tx_type=tx_type,
        received_amount="",
        received_currency="",
        sent_amount=sent_amount,
        sent_currency=sent_currency,
        fee=fee,
        fee_currency=fee_currency,
        exchange=txinfo.exchange,
        wallet_address=txinfo.wallet_address,
        txid=txinfo.txid,
        url=txinfo.url,
        z_index=z_index,
        comment=txinfo.comment,
    )


def _make_tx_exchange(txinfo, sent_amount, sent_currency, received_amount, received_currency, tx_type, txid=None, empty_fee=False, z_index=0):
    """
    Helper function to create a transaction for a token exchange.
    """
    txid = txid if txid else txinfo.txid
    fee = "" if empty_fee else txinfo.fee
    fee_currency = txinfo.fee_currency if fee else ""

    return Row(
        timestamp=txinfo.timestamp,
        tx_type=tx_type,
        received_amount=received_amount,
        received_currency=received_currency,
        sent_amount=sent_amount,
        sent_currency=sent_currency,
        fee=fee,
        fee_currency=fee_currency,
        exchange=txinfo.exchange,
        wallet_address=txinfo.wallet_address,
        txid=txid,
        url=txinfo.url,
        z_index=z_index,
        comment=txinfo.comment,
    )
