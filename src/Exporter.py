import os
import csv
from datetime import datetime
from src.ErrorCounter import ErrorCounter

# Initialize the error counter
error_counter = ErrorCounter()

class Exporter:
    def __init__(self, wallet_address, transactions):
        self.wallet_address = wallet_address
        self.transactions = transactions

    def export(self, export_format):
        """
        Exports transactions based on the specified format.
        """
        if export_format == "koinly":
            self._export_to_koinly()
        elif export_format == "cryptotax":
            self._export_to_cryptotax()
        elif export_format == "other_format":
            self._export_to_other()
        else:
            error_counter.increment("UNSUPPORTED_FORMAT")
            raise ValueError(f"Unsupported format: {export_format}")

    def _export_to_koinly(self):
        file_path = os.path.join("reports", f"voi_{self.wallet_address}_koinly.csv")
        self._write_csv(file_path, [
            "Date", "Sent Amount", "Sent Currency", "Received Amount", 
            "Received Currency", "Fee Amount", "Fee Currency", 
            "Net Worth Amount", "Net Worth Currency", "Label", 
            "Description", "TxHash"
        ], self._format_koinly_row)
        print(f"Koinly CSV exported to {file_path}")

    def _export_to_cryptotax(self):
        file_path = os.path.join("reports", f"voi_{self.wallet_address}_cryptotax.csv")
        self._write_csv(file_path, [
            "Date", "Transaction Type", "Base Currency", "Base Amount", 
            "Quote Currency", "Quote Amount", "Fee Currency", "Fee Amount"
        ], self._format_cryptotax_row)
        print(f"Cryptotax CSV exported to {file_path}")

    def _export_to_other(self):
        file_path = os.path.join("reports", f"voi_{self.wallet_address}_other_format.csv")
        self._write_csv(file_path, [
            "Date", "Transaction Type", "Currency", "Amount", "Fee", "TxHash"
        ], self._format_other_row)
        print(f"Other Format CSV exported to {file_path}")

    def _write_csv(self, file_path, header, row_formatter):
        """
        Generic method to write transactions to a CSV file.
        """
        try:
            with open(file_path, mode="w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(header)
                for tx in self.transactions:
                    try:
                        row = row_formatter(tx)
                        writer.writerow(row)
                    except KeyError as e:
                        error_counter.increment("ROW_FORMAT_ERROR")
                        print(f"Error formatting row: {e}")
        except Exception as e:
            error_counter.increment("FILE_WRITE_ERROR")
            print(f"Error writing CSV file: {e}")

    def _format_koinly_row(self, tx):
        return [
            self._format_date(tx.get("timestamp")),
            tx.get("sent_amount", ""),
            tx.get("sent_currency", "VOI"),
            tx.get("received_amount", ""),
            tx.get("received_currency", "VOI"),
            tx.get("fee", ""),
            tx.get("fee_currency", "VOI"),
            tx.get("net_worth_amount", ""),
            tx.get("net_worth_currency", ""),
            tx.get("label", ""),
            tx.get("description", "VOI transaction"),
            tx.get("tx_hash", "")
        ]

    def _format_cryptotax_row(self, tx):
        return [
            self._format_date(tx.get("timestamp")),
            tx.get("transaction_type", "transfer"),
            tx.get("base_currency", "VOI"),
            tx.get("base_amount", ""),
            tx.get("quote_currency", ""),
            tx.get("quote_amount", ""),
            tx.get("fee_currency", "VOI"),
            tx.get("fee", "")
        ]

    def _format_other_row(self, tx):
        return [
            self._format_date(tx.get("timestamp")),
            tx.get("transaction_type", "transfer"),
            tx.get("currency", "VOI"),
            tx.get("amount", ""),
            tx.get("fee", ""),
            tx.get("tx_hash", "")
        ]

    def _format_date(self, timestamp):
        """
        Format timestamp to ISO 8601 date string.
        """
        try:
            return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            error_counter.increment("DATE_FORMAT_ERROR")
            return "Invalid Date"


def ensure_reports_directory():
    """
    Ensure the reports directory exists.
    """
    os.makedirs("reports", exist_ok=True)
