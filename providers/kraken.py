import requests

from provider_base import Provider
from coin import Coins


class KrakenProvider(Provider):
    """Kraken exchange API provider for cryptocurrency market data.
    
    Public API that doesn't require authentication for ticker data.
    Note: Kraken uses different symbol naming (e.g., XBT instead of BTC).
    """
    name = "Kraken"

    URL = "https://api.kraken.com/0/public/Ticker"

    def __init__(self):
        """Initialize provider with session for connection pooling."""
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "tether-monitor/1.0"})

    def fetch(self, currency: str = "USD") -> Coins:
        """Fetch coin data from Kraken API.
        
        Args:
            currency: Quote currency for trading pairs (e.g., 'USD', 'EUR').
            
        Returns:
            Coins collection with market data.
            
        Raises:
            RuntimeError: If the API request fails.
        """
        # Kraken uses specific pair names. For simplicity, we'll fetch a few major pairs.
        # Map common symbols to Kraken's naming convention
        pairs = {
            "USD": ["XBTUSD", "ETHUSD"],
            "EUR": ["XBTEUR", "ETHEUR"],
        }
        
        target_pairs = pairs.get(currency.upper(), pairs["USD"])
        
        try:
            response = self.session.get(self.URL, params={"pair": ",".join(target_pairs)}, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Kraken API error: {e}") from e

        if data.get("error"):
            raise RuntimeError(f"Kraken API error: {', '.join(data['error'])}")

        coins_data = []
        result = data.get("result", {})
        
        # Map Kraken symbols back to standard symbols
        symbol_map = {
            "XXBTZUSD": "BTC",
            "XETHZUSD": "ETH",
            "XRPXXBT": "XRP",
            "LTCXXBT": "LTC",
            "XXBTZEUR": "BTC",
            "XETHZEUR": "ETH",
        }

        for pair_name, ticker in result.items():
            standard_symbol = symbol_map.get(pair_name, pair_name)
            
            # Kraken ticker structure
            close = ticker.get("c", ["0"])[0]  # Last trade closed
            open_price = ticker.get("o", "0")  # Today's opening price
            high = ticker.get("h", ["0"])[0]  # Today's high
            low = ticker.get("l", ["0"])[0]  # Today's low
            volume = ticker.get("v", ["0"])[0]  # Today's volume
            
            # Calculate 24h change
            try:
                price_change = ((float(close) - float(open_price)) / float(open_price)) * 100
            except (ValueError, ZeroDivisionError):
                price_change = 0

            coins_data.append({
                "name": standard_symbol,
                "symbol": standard_symbol,
                "current_price": close,
                "price_change_24h": price_change,
                "high_24h": high,
                "low_24h": low,
                "market_cap": None,  # Kraken doesn't provide market cap in ticker
                "volume_24h": volume,
                "circulating_supply": None,  # Kraken doesn't provide supply
                "rank": None,  # Kraken doesn't provide rank
            })

        return Coins.from_list(self.name, currency, coins_data)
