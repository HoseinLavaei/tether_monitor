import requests

from provider_base import Provider
from coin import Coins


class NobitexProvider(Provider):
    """Nobitex exchange API provider for Iranian cryptocurrency market.

    Supports Iranian Rial (RLS) as quote currency.
    """
    name = "Nobitex"

    URL = "https://apiv2.nobitex.ir/market/stats"

    def __init__(self):
        """Initialize provider with session for connection pooling."""
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "tether-monitor/1.0"})

    def fetch(self, currency: str = "RLS") -> Coins:
        """Fetch coin data from Nobitex API.
        
        Args:
            currency: Quote currency (default: 'RLS' for Iranian Rial).
            
        Returns:
            Coins collection with market data.
            
        Raises:
            RuntimeError: If the API request fails.
        """
        # Nobitex uses specific currency codes. Major trading pairs:
        # BTC-RLS, ETH-RLS, LTC-RLS, USDT-RLS, BNB-RLS, XRP-RLS
        symbols = ["btc", "eth", "ltc", "usdt", "bnb", "xrp"]
        
        coins_data = []
        
        for symbol in symbols:
            try:
                params = {
                    "srcCurrency": symbol,
                    "dstCurrency": currency.lower(),
                }
                
                response = self.session.get(self.URL, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                if data.get("status") != "ok":
                    continue
                    
                stats = data.get("stats", {})
                market_key = f"{symbol}-{currency.lower()}"
                market_data = stats.get(market_key)
                
                if not market_data:
                    continue
                
                # Calculate 24h change percentage
                day_change = market_data.get("dayChange", "0")
                
                coins_data.append({
                    "name": symbol.upper(),
                    "symbol": symbol.upper(),
                    "current_price": market_data.get("latest", "0"),
                    "price_change_24h": day_change,
                    "high_24h": market_data.get("dayHigh", "0"),
                    "low_24h": market_data.get("dayLow", "0"),
                    "market_cap": None,  # Nobitex doesn't provide market cap
                    "volume_24h": market_data.get("volumeDst", "0"),
                    "circulating_supply": None,  # Nobitex doesn't provide supply
                    "rank": None,  # Nobitex doesn't provide rank
                    "currency": currency,
                     "provider" : self.name
                })
                
            except requests.RequestException:
                # Skip this symbol if request fails, continue with others
                continue

        return Coins.from_list(coins_data)
