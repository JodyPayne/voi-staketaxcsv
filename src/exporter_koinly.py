import json
import logging
import os

from staketaxcsv.common.Cache import Cache
from staketaxcsv import settings_csv

# Path to the Koinly null map file
KOINLY_NULL_MAP_JSON = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../_reports/koinly_null_map.json")
LOCAL_MAP = "local_map"


class NullMap:
    """
    Handles Koinly-compatible null mappings for symbols.
    """
    def __init__(self, json_path=None):
        self.null_map = []
        self.cache = None
        self.use_cache = settings_csv.DB_CACHE
        self.json_path = json_path if json_path else KOINLY_NULL_MAP_JSON

        logging.info("Koinly NullMap: use_cache=%s, json_path=%s", self.use_cache, self.json_path)

    def _cache(self):
        if not self.cache:
            self.cache = Cache()
        return self.cache

    def load(self):
        """
        Load null mappings from cache or JSON file.
        """
        if self.use_cache:
            self.null_map = self._cache().get_koinly_null_map()
            if not self.null_map:
                self.null_map = []
        else:
            if self.json_path == LOCAL_MAP:
                self.null_map = []
            else:
                if self.json_path and os.path.exists(self.json_path):
                    with open(self.json_path, 'r') as f:
                        self.null_map = json.load(f)

    def flush(self):
        """
        Save null mappings to cache or JSON file.
        """
        if self.use_cache:
            self._cache().set_koinly_null_map(self.null_map)
        else:
            if self.json_path == LOCAL_MAP:
                return
            else:
                if self.json_path:
                    with open(self.json_path, 'w') as f:
                        json.dump(self.null_map, f, indent=4)

    def get_null_symbol(self, symbol):
        """
        Get or assign a null symbol for a given asset or token.
        """
        if symbol not in self.null_map:
            self.null_map.append(symbol)

        index = self.null_map.index(symbol)

        # Koinly requires indices > 0
        return f"NULL{index + 1}"

    def list_for_display(self):
        """
        Prepare a list of null mappings for display purposes.
        """
        self.load()

        out = []
        for index in range(len(self.null_map)):
            out.append((f"NULL{index + 1}", self.null_map[index]))
        return out
