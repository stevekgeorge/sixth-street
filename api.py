from cache import Cache
import requests

class AlphaVantageAPI:
    """
    Class for interacting with Alpha Vantage API
    
    Attributes:
        cache_dir (str): Directory path for caching responses
        base (str): Base URL for requests
        api_key (str): Key for accessing the API
    """

    def __init__(self, cache_dir='cache', api_key=None):
        """
        Initializes the AlphaVantageAPI instance

        Args:
            cache_dir (str, optional): Path that defaults to 'cache'
            api_key (str, optional): API key that defaults to None
        """
        self.cache = Cache(cache_dir)
        self.base = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'
        self.api_key = api_key

    def _process_time_series(self, time_series):
        """
        Process time series data

        Args:
            time_series (dict): Raw time series data

        Returns:
            dict: Processed time series data
        """

        
        processed_data = {}
        for date, data in time_series.items():
            processed_data[date] = {
                'open': float(data['1. open']),
                'high': float(data['2. high']),
                'low': float(data['3. low']),
                'close': float(data['4. close']),
                'volume': int(data['5. volume'])
            }

        return processed_data

    def get_time_series(self, symbol, outputsize='full'):
        """
        Retrieves time series data for a specific symbol

        Args:
            symbol (str): Stock symbol
            outputsize (str, optional): Size of the data (compact/full) and defaults to 'full'

        Returns:
            dict: Time series data
        """
        if self.cache.check_cache(symbol):
            return self.cache.get(symbol)

        url = f'{self.base}&symbol={symbol}&outputsize={outputsize}&apikey={self.api_key}'
        req = requests.get(url)
        data = req.json()

        if 'Error Message' in data:
            return False

        time_series = self._process_time_series(data['Time Series (Daily)'])
        self.cache.set(symbol, time_series)
        return time_series

    def get_lookup(self, symbol, date):
        """
        Retrieves data for a specific symbol and date from time series

        Args:
            symbol (str): Stock symbol
            date (str): Date for which data is requested (YYYY-MM-DD)

        Returns:
            dict: Data for specified symbol and date
        """
        time_series = self.get_time_series(symbol)

        if not time_series:
            return {'Error': 'Symbol not found'}

        if date not in time_series:
            return {'Error': 'Date not found'}

        return time_series[date]


    def get_min(self, symbol, n):
        """
        Retrieves minimum price for a symbol over the 'n' days

        Args:
            symbol (str): Stock symbol
            n (int): Number of days

        Returns:
            dict: Minimum price and corresponding date
        """
        time_series = self.get_time_series(symbol)

        if not time_series:
            return {'Error': 'Symbol not found'}

        if n > len(time_series):
            return {'Error': 'Not enough data'}

        min_price = float('inf')
        first_n = list(time_series.items())[:n]
        for date, data in first_n:
            if data['low'] < min_price:
                min_price = data['low']

        return {'min': min_price}


    def get_max(self, symbol, n):
        """
        Retrieves maximum price for a symbol over last 'n' days

        Args:
            symbol (str): Stock symbol
            n (int): Number of days

        Returns:
            dict: Maximum price and corresponding date
        """
        time_series = self.get_time_series(symbol)

        if not time_series:
            return {'Error': 'Symbol not found'}

        if n > len(time_series):
            return {'Error': 'Not enough data'}

        max_price = 0
        first_n = list(time_series.items())[:n]
        for date, data in first_n:
            if data['high'] > max_price:
                max_price = data['high']

        return {'max': max_price}