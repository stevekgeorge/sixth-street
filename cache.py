import json
from datetime import datetime

class Cache():
    """
    A cache for storing and retrieving data as JSON files

    Attributes:
        cache_dir (str): Directory path where cache files are stored
    """

    def __init__(self, cache_dir='cache'):
        """
        Initializes the Cache object

        Args:
            cache_dir (str, optional): Path for storing cache files and defaults to 'cache'
        """
        self.cache_dir = cache_dir

    def _get_today(self):
        """
        Retrieves the current date in YYYY-MM-DD format

        Returns:
            str: Current date in YYYY-MM-DD format
        """
        return datetime.now().strftime('%Y-%m-%d')

    def check_cache(self, symbol):
        """
        Checks if cache exists and if it's up to date for a given symbol

        Args:
            symbol (str): Symbol for which cache is checked

        Returns:
            bool: True if cache exists and is up to date, False otherwise
        """
        if symbol not in self.cache_dir:
            return False

        with open(f'{self.cache_dir}/{symbol}.json', 'r') as f:
            data = json.load(f)

        last_day = list(data.keys())[0]
        if last_day != self._get_today():
            return False

        return True

    def set(self, symbol, data):
        """
        Sets data into the cache file for a given symbol

        Args:
            symbol (str): Symbol for which data is cached
            data (dict): Data to be cached

        Returns:
            bool: True if data is successfully cached, False otherwise
        """
        try:
            with open(f'{self.cache_dir}/{symbol}.json', 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f'Error: {e}')
            return False

    def get(self, symbol):
        """
        Retrieves data from the cache file for a given symbol

        Args:
            symbol (str): Symbol for which data is retrieved

        Returns:
            dict or False: Cached data if found and up to date, False otherwise
        """
        if self.check_cache(symbol):
            with open(f'{self.cache_dir}/{symbol}.json', 'r') as f:
                data = json.load(f)
            return data

        return False
