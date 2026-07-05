import requests

from coin import Coins
from provider_base import Provider


class BitpinProvider(Provider):
    """Bitpin API provider for cryptocurrency market data.

    Fetches market data for trading pairs. Bitpin does not provide market cap,
    circulating supply, or rank information.
    """

    name = "Bitpin"

    SUPPORTED_QUOTES = {"IRT", "USDT"}

    def __init__(self):
        """Initialize provider with session for connection pooling."""
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "tether-monitor/1.0"})

    def fetch(self, currency: str = "IRT") -> Coins:
        """Fetch coin data from the Bitpin API.

        Args:
            currency: Quote currency (e.g. "IRT", "USDT").

        Returns:
            Coins collection with market data.

        Raises:
            ValueError: If the currency is not supported.
            RuntimeError: If the API request fails.
        """
        currency = currency.upper()

        if currency not in self.SUPPORTED_QUOTES:
            raise ValueError(
                f"Unsupported currency: {currency}. "
                f"Supported: {self.SUPPORTED_QUOTES}"
            )

        url = "https://api.bitpin.ir/v1/mkt/markets/"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()["results"]
        except requests.RequestException as e:
            raise RuntimeError(f"Bitpin API error: {e}") from e

        coins_data = [
            {
                "name": market["currency1"]["title"],
                "symbol": market["currency1"]["code"].upper(),
                "current_price": market["price"],
                "price_change_24h": market["price_info"]["change"],
                "high_24h": market["price_info"]["max"],
                "low_24h": market["price_info"]["min"],
                "market_cap": None,
                "volume_24h": market["price_info"]["value"],
                "circulating_supply": None,
                "rank": None,
                "currency": currency,
                "provider": self.name,
            }
            for market in data
            if market["currency2"]["code"].upper() == currency
        ]

        return Coins.from_list(coins_data)