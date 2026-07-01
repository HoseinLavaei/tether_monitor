import requests

from provider_base import Provider
from coin import Coins


class BinanceProvider(Provider):
    """Binance API provider for cryptocurrency market data.
    
    Fetches 24h ticker data for trading pairs. Note: Binance does not provide
    market cap, circulating supply, or rank information.
    """
    name = "Binance"

    SUPPORTED_QUOTES = {"USDT", "BUSD", "USDC", "BTC", "ETH", "FDUSD"}

    def __init__(self):
        """Initialize provider with session for connection pooling."""
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "tether-monitor/1.0"})

    def fetch(self, currency: str = "USDT") -> Coins:
        """Fetch coin data from Binance API.
        
        Args:
            currency: Quote currency for trading pairs (e.g., 'USDT', 'BTC').
            
        Returns:
            Coins collection with market data.
            
        Raises:
            ValueError: If the currency is not supported.
            RuntimeError: If the API request fails.
        """
        currency = currency.upper()
        
        if currency not in self.SUPPORTED_QUOTES:
            raise ValueError(f"Unsupported currency: {currency}. Supported: {self.SUPPORTED_QUOTES}")

        url = "https://api.binance.com/api/v3/ticker/24hr"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Binance API error: {e}") from e

        coins_data = [
            {
                "name": item["symbol"][:-len(currency)],
                "symbol": item["symbol"][:-len(currency)],
                "current_price": item["lastPrice"],
                "price_change_24h": item["priceChangePercent"],
                "high_24h": item["highPrice"],
                "low_24h": item["lowPrice"],
                "market_cap": None,
                "volume_24h": item["quoteVolume"],
                "circulating_supply": None,
                "rank": None,
            }
            for item in data
            if item["symbol"].endswith(currency)
        ]

        return Coins.from_list(self.name, currency, coins_data)