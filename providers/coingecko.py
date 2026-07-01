import requests

from provider_base import Provider
from coin import Coins


class CoinGeckoProvider(Provider):
    """CoinGecko API provider for cryptocurrency market data."""
    name = "CoinGecko"

    URL = "https://api.coingecko.com/api/v3/coins/markets"

    def __init__(self, per_page: int = 10):
        """Initialize provider with configurable pagination.
        
        Args:
            per_page: Number of coins to fetch per request (default: 10).
        """
        self.per_page = per_page
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "tether-monitor/1.0"})

    def fetch(self, currency: str = "usd") -> Coins:
        """Fetch coin data from CoinGecko API.
        
        Args:
            currency: Target currency code (e.g., 'usd', 'eur').
            
        Returns:
            Coins collection with market data.
            
        Raises:
            RuntimeError: If the API request fails.
        """
        params = {
            "vs_currency": currency.lower(),
            "order": "market_cap_desc",
            "per_page": self.per_page,
            "page": 1,
            "sparkline": "false",
        }

        try:
            response = self.session.get(self.URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"CoinGecko API error: {e}") from e

        coins_data = [
            {
                "name": item["name"],
                "symbol": item["symbol"].upper(),
                "current_price": item["current_price"],
                "price_change_24h": item["price_change_percentage_24h"],
                "high_24h": item["high_24h"],
                "low_24h": item["low_24h"],
                "market_cap": item.get("market_cap"),
                "volume_24h": item["total_volume"],
                "circulating_supply": item.get("circulating_supply"),
                "rank": item["market_cap_rank"],
            }
            for item in data
        ]

        return Coins.from_list(self.name, currency, coins_data)