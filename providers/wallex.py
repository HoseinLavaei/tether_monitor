import requests

from coin import Coins
from provider_base import Provider


class WallexProvider(Provider):
    """Wallex API provider."""

    name = "Wallex"

    SUPPORTED_QUOTES = {"TMN", "USDT"}

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "tether-monitor/1.0"
        })

    @staticmethod
    def _optional(value):
        """Convert Wallex's placeholder values to None."""
        if value in ("-", "", None):
            return None
        return value

    def fetch(self, currency: str = "TMN") -> Coins:
        currency = currency.upper()

        if currency not in self.SUPPORTED_QUOTES:
            raise ValueError(
                f"Unsupported currency: {currency}. "
                f"Supported: {self.SUPPORTED_QUOTES}"
            )

        url = "https://api.wallex.ir/v1/markets"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()["result"]["symbols"]
        except requests.RequestException as e:
            raise RuntimeError(f"Wallex API error: {e}") from e

        coins_data = []

        for market in data.values():
            if market["quoteAsset"].upper() != currency:
                continue

            stats = market["stats"]

            # If there is no current price at all, ignore this market.
            if stats["lastPrice"] == "-":
                continue

            coins_data.append({
                "name": market["enBaseAsset"],
                "symbol": market["baseAsset"].upper(),

                "current_price": stats["lastPrice"],

                "price_change_24h": self._optional(stats["24h_ch"]),
                "high_24h": self._optional(stats["24h_highPrice"]),
                "low_24h": self._optional(stats["24h_lowPrice"]),

                "market_cap": None,

                "volume_24h": self._optional(stats["24h_quoteVolume"]),

                "circulating_supply": None,
                "rank": None,

                "currency": currency,
                "provider": self.name,
            })

        return Coins.from_list(coins_data)