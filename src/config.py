from staketaxcsv.common import ExporterTypes as et

class Config:
    """
    Configuration class for the VOI exporter.
    """
    # Job context (can hold relevant export job-specific metadata)
    job = None

    # Debug mode (set to True for verbose logging)
    debug = False

    # Maximum number of transactions to fetch per API call
    limit = 20000  # Adjust as necessary for VOI API limits

    # Null mapping for Koinly (used to replace null values in the export)
    koinlynullmap = None

    # Default node settings for VOI API interaction
    node_settings = {
        "algod_url": "https://mainnet-api.voi.nodely.dev",
        "algod_port": 443,
        "indexer_url": "https://mainnet-idx.voi.nodely.dev",
        "indexer_port": 443,
    }

    @classmethod
    def get_node_setting(cls, key):
        """
        Retrieve node settings like API URLs and ports.
        """
        return cls.node_settings.get(key)

    @classmethod
    def is_debug(cls):
        """
        Check if debug mode is enabled.
        """
        return cls.debug

    @classmethod
    def set_debug(cls, debug_value):
        """
        Enable or disable debug mode.
        """
        cls.debug = debug_value

    @classmethod
    def get_limit(cls):
        """
        Get the transaction limit for API requests.
        """
        return cls.limit
