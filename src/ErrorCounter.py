import logging


class ErrorCounter:
    """
    Tracks and logs errors that occur during the transaction export process.
    """
    errors = {}

    @classmethod
    def increment(cls, error_type, txid=None):
        """
        Increment the count of a specific error type.

        Args:
            error_type (str): The type of error encountered.
            txid (str, optional): The transaction ID associated with the error.
        """
        cls.errors[error_type] = cls.errors.get(error_type, 0) + 1

        if txid:
            logging.error("Unable to handle txid=%s with error_type=%s", txid, error_type)
        else:
            logging.error("Error encountered with error_type=%s", error_type)

    @classmethod
    def log(cls, ticker, wallet_address):
        """
        Log the accumulated error counts along with ticker and wallet information.

        Args:
            ticker (str): The cryptocurrency ticker (e.g., VOI).
            wallet_address (str): The wallet address being processed.
        """
        if cls.errors:
            data = {
                "ticker": ticker,
                "wallet_address": wallet_address,
                "error_count": cls.errors,
                "RLOG": 1,
                "event": "job_error_count"
            }
            logging.info("Error summary: %s", data)

    @classmethod
    def clear(cls):
        """
        Reset the error counts.
        """
        cls.errors = {}
        logging.info("ErrorCounter reset.")
