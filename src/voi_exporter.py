import argparse
import os
import csv
import json
import requests
from datetime import datetime, timezone
from ExporterTypes import TX_TYPE_TRANSFER, TX_TYPE_TRADE, TX_TYPE_STAKING, TX_TYPE_INCOME
from ErrorCounter import ErrorCounter
import base64  # For decoding transaction notes

# Initialize the error counter
error_counter = ErrorCounter()


def get_data_path(file_name):
    """
    Dynamically resolves the absolute path for a file in the 'data' directory.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "data", file_name)


def fetch_asset_info(asset_id):
    """
    Fetch dynamic asset information (name, decimals) from the VOI API.
    """
    url = f"https://mainnet-idx.voi.nodely.dev/v2/assets/{asset_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        asset_data = response.json()
        return {
            "unit-name": asset_data.get("params", {}).get("unit-name", f"Asset-{asset_id}"),
            "decimals": asset_data.get("params", {}).get("decimals", 0),
        }
    except requests.RequestException as e:
        error_counter.increment("ASSET_INFO_ERROR", asset_id)
        print(f"Error fetching asset info for {asset_id}: {e}")
        return {"unit-name": f"Asset-{asset_id}", "decimals": 0}


def fetch_transactions(wallet_address):
    """
    Fetch transactions for the given wallet address using the VOI API.
    """
    indexer_url = "https://mainnet-idx.voi.nodely.dev/v2/accounts"
    try:
        response = requests.get(f"{indexer_url}/{wallet_address}/transactions", params={"limit": 1000})
        response.raise_for_status()
        transactions = response.json().get("transactions", [])
        print(f"Fetched {len(transactions)} transactions for wallet {wallet_address}.")
        return transactions
    except requests.RequestException as e:
        error_counter.increment("API_ERROR", wallet_address)
        print(f"Error fetching transactions: {e}")
        return []


def decode_base64(data):
    """
    Decode a base64 encoded string.
    """
    try:
        return base64.b64decode(data).decode("utf-8")
    except Exception as e:
        return f"Decoding failed: {e}"


def parse_global_state_delta(tx):
    """
    Parse the `global-state-delta` for meaningful data.
    """
    global_state_delta = tx.get("global-state-delta", [])
    parsed_data = {}
    for delta in global_state_delta:
        key = delta.get("key")
        value = delta.get("value", {}).get("uint", 0)
        if key:
            try:
                decoded_key = decode_base64(key)
                parsed_data[decoded_key] = value
            except Exception as e:
                print(f"Error decoding global-state-delta key: {e}")
    return parsed_data


def format_date(timestamp):
    """
    Convert timestamp to a human-readable date format (ISO 8601).
    """
    try:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        error_counter.increment("DATE_ERROR", timestamp)
        return "1970-01-01 00:00:00"


def write_csv(file_path, header, rows):
    """
    Write rows of data to a CSV file.
    """
    try:
        with open(file_path, mode="w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerows(rows)
        print(f"CSV exported to {file_path}")
    except IOError as e:
        error_counter.increment("FILE_WRITE_ERROR", file_path)
        print(f"Error writing to file {file_path}: {e}")


def export_to_koinly(transactions, wallet_address, tokens, reports_dir):
    """
    Export transactions to the Koinly CSV format.
    """
    file_path = os.path.join(reports_dir, f"voi_{wallet_address}_koinly.csv")
    header = [
        "Date", "Sent Amount", "Sent Currency", "Received Amount",
        "Received Currency", "Fee Amount", "Fee Currency", "Net Worth Amount",
        "Net Worth Currency", "Label", "Description", "TxHash", "Asset ID", "Price (USD)"
    ]
    rows = []

    for tx in transactions:
        tx_hash = tx.get("id", "")
        sender = tx.get("sender", "")
        receiver = tx.get("payment-transaction", {}).get("receiver", "")
        asset_id = str(tx.get("asset-transfer-transaction", {}).get("asset-id", 0))
        asset_info = tokens.get(asset_id, fetch_asset_info(asset_id))
        currency = asset_info["unit-name"]
        decimals = asset_info["decimals"]

        amount = tx.get("payment-transaction", {}).get("amount", 0) / 10 ** decimals
        if tx.get("asset-transfer-transaction"):
            amount = tx.get("asset-transfer-transaction", {}).get("amount", 0) / 10 ** decimals

        fee = tx.get("fee", 0) / 1e6
        date = format_date(tx.get("round-time", 0))
        label = "sent" if sender == wallet_address else "received"

        note = decode_base64(tx.get("note", ""))
        global_state_data = parse_global_state_delta(tx)

        description = note if note else f"Transaction involving {currency}"
        if global_state_data:
            description += f" | Global State: {global_state_data}"

        rows.append([
            date,
            amount if label == "sent" else "",
            currency,
            amount if label == "received" else "",
            currency,
            fee,
            currency,
            "",  # Net Worth Amount left blank
            "USD",
            label,
            description,
            tx_hash,
            asset_id
        ])

    write_csv(file_path, header, rows)


def export_data(format, wallet_address):
    """
    Export transaction data for the specified format and wallet address.
    """
    reports_dir = os.path.abspath("reports")
    os.makedirs(reports_dir, exist_ok=True)

    tokens_file_path = get_data_path("voi_tokens.json")
    try:
        with open(tokens_file_path, "r") as f:
            tokens = json.load(f).get("tokens", {})
    except FileNotFoundError:
        tokens = {}
        error_counter.increment("FILE_ERROR", wallet_address)
        print(f"Error: The '{tokens_file_path}' file does not exist. Using dynamic asset fetching.")

    transactions = fetch_transactions(wallet_address)
    if not transactions:
        print("No transactions found for the given wallet.")
        return

    if format == "koinly":
        export_to_koinly(transactions, wallet_address, tokens, reports_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VOI Exporter")
    parser.add_argument("--format", required=True, help="Specify the export format (e.g., koinly)")
    parser.add_argument("--wallet", required=True, help="Specify the wallet address")
    args = parser.parse_args()

    export_data(args.format, args.wallet)
