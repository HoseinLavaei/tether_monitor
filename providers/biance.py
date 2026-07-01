from decimal import Decimal

import requests
from typing import Any

from provider_base import Provider
from coin import Coins


class BinanceProvider(Provider):
    name = "Binance"

    def __init__(self):
        self.quotes = {"USDT", "BUSD", "USDC", "BTC", "ETH", "FDUSD"}

    def fetch(self, currency: str = "USDT") -> Coins:
        url = "https://api.binance.com/api/v3/ticker/24hr"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        currency = currency.upper()
        coins_data: list[dict[str, Any]] = []

        for item in data:
            symbol = item.get("symbol", "")

            quote = next(
                (q for q in self.quotes if symbol.endswith(q)),
                None
            )

            if quote != currency:
                continue

            base = symbol[:-len(quote)]

            coins_data.append({
                "name": base,
                "symbol": base,
                "current_price": Decimal(item["lastPrice"]),
                "price_change_24h": Decimal(item["priceChangePercent"]),
                "high_24h": Decimal(item["highPrice"]),
                "low_24h": Decimal(item["lowPrice"]),
                "market_cap": None,
                "volume_24h": Decimal(item["quoteVolume"]),
                "circulating_supply": None,
                "rank": None,
            })

        return Coins.from_list(self.name, currency, coins_data)