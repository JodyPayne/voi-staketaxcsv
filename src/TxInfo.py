class TxInfo:
    """
    Represents the information of a single transaction.
    """

    def __init__(self, txid, timestamp, fee, fee_currency, wallet_address, exchange, url):
        self.txid = txid  # Unique transaction ID
        self.timestamp = timestamp  # Transaction timestamp in UNIX epoch time
        self.fee = fee  # Fee amount for the transaction
        self.fee_currency = fee_currency  # Currency used for the fee (e.g., VOI)
        self.wallet_address = wallet_address  # Address associated with the wallet
        self.exchange = exchange  # Exchange or blockchain name
        self.url = url  # URL for viewing the transaction on a block explorer

        # Optional fields for extended details
        self.comment = ""  # Additional comments or notes
        self.memo = ""  # Memo or label associated with the transaction
        self.sent_amount = ""  # Amount sent in the transaction
        self.sent_currency = ""  # Currency sent in the transaction
        self.received_amount = ""  # Amount received in the transaction
        self.received_currency = ""  # Currency received in the transaction
        self.net_worth_amount = ""  # Net worth amount, if applicable
        self.net_worth_currency = ""  # Net worth currency, if applicable
        self.tx_type = ""  # Type of the transaction (e.g., trade, transfer, staking)
        self.label = ""  # Label for the transaction (e.g., sent, received, income)

    def set_sent(self, amount, currency):
        """
        Set details for the sent amount and currency.
        """
        self.sent_amount = amount
        self.sent_currency = currency

    def set_received(self, amount, currency):
        """
        Set details for the received amount and currency.
        """
        self.received_amount = amount
        self.received_currency = currency

    def set_net_worth(self, amount, currency):
        """
        Set net worth details, if applicable.
        """
        self.net_worth_amount = amount
        self.net_worth_currency = currency

    def set_label(self, label):
        """
        Set the transaction label (e.g., sent, received, income, etc.).
        """
        self.label = label

    def to_dict(self):
        """
        Convert transaction info to a dictionary for easier CSV writing.
        """
        return {
            "txid": self.txid,
            "timestamp": self.timestamp,
            "fee": self.fee,
            "fee_currency": self.fee_currency,
            "wallet_address": self.wallet_address,
            "exchange": self.exchange,
            "url": self.url,
            "comment": self.comment,
            "memo": self.memo,
            "sent_amount": self.sent_amount,
            "sent_currency": self.sent_currency,
            "received_amount": self.received_amount,
            "received_currency": self.received_currency,
            "net_worth_amount": self.net_worth_amount,
            "net_worth_currency": self.net_worth_currency,
            "tx_type": self.tx_type,
            "label": self.label,
        }
