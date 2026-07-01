import requests

from provider_base import Provider
from coin import Coins


class AbanTetherProvider(Provider):
    """AbanTether exchange API provider.

    Supports Iranian Rial (IRT) markets.
    """

    name = "AbanTether"

    URL = "https://api.abantether.com/api/v1/manager/otc/ticker"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "tether-monitor/1.0"
        })

    def fetch(self, currency: str = "IRT") -> Coins:
        if currency.upper() != "IRT":
            raise ValueError(
                "AbanTether only supports the IRT market."
            )

        response = self.session.get(self.URL, timeout=30)
        response.raise_for_status()

        data = response.json()

        markets = data["data"]["markets"]

        coins_data = []

        for market in markets.values():
            if not market["active"]:
                continue

            coins_data.append({
                "provider": self.name,
                "currency": "IRT",

                "name": market["symbol"],
                "symbol": market["symbol"],

                # AbanTether exposes buy/sell prices.
                # We use the buy price as the current market price.
                "current_price": market["buy_price"],

                # This endpoint does not expose 24h statistics.
                "price_change_24h": None,
                "high_24h": None,
                "low_24h": None,
                "volume_24h": None,

                "market_cap": None,
                "circulating_supply": None,
                "rank": None,
            })

        return Coins.from_list(coins_data)