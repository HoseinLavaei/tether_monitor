from decimal import Decimal

import requests
from provider_base import Provider
from coin import Coins


class CoinGeckoProvider(Provider):
    name = "CoinGecko"

    URL = "https://api.coingecko.com/api/v3/coins/markets"

    def fetch(self, currency: str = "usd") -> Coins:
        params = {
            "vs_currency": currency.lower(),
            "order": "market_cap_desc",
            "per_page": 10,
            "page": 1,
            "sparkline": "false",
        }

        response = requests.get(self.URL, params=params)
        response.raise_for_status()

        data = response.json()

        coins_data = []

        for item in data:
            coins_data.append({
                "name": item["name"],
                "symbol": item["symbol"].upper(),
                "current_price": Decimal(str(item["current_price"])),
                "price_change_24h": Decimal(str(item["price_change_percentage_24h"])),
                "high_24h": Decimal(str(item["high_24h"])),
                "low_24h": Decimal(str(item["low_24h"])),
                "market_cap": Decimal(str(item.get("market_cap"))),
                "volume_24h": Decimal(str(item["total_volume"])),
                "circulating_supply": Decimal(str(item.get("circulating_supply"))),
                "rank": int(item["market_cap_rank"]),
            })

        return Coins.from_list(self.name, currency, coins_data)