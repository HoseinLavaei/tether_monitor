from providers.coingecko import CoinGeckoProvider
from providers.binance import BinanceProvider
from providers.kraken import KrakenProvider
from providers.nobitex import NobitexProvider

def main():
    gecko = CoinGeckoProvider()
    binance = BinanceProvider()
    kraken = KrakenProvider()
    nobitex = NobitexProvider()

    # Try multiple currencies
    currencies = ["USD", "EUR"]

    for currency in currencies:
        print(f"\n\n############################")
        print(f"Currency: {currency}")
        print(f"############################")

        # CoinGecko supports real fiat currencies
        gecko_coins = gecko.fetch(currency.lower())

        # Binance only really uses USDT-style markets
        binance_coins = binance.fetch("USDT")

        # Kraken supports multiple currencies
        kraken_coins = kraken.fetch(currency)

        btc_gecko = gecko_coins.get("CoinGecko", currency.lower(), "BTC")
        btc_binance = binance_coins.get("Binance", "USDT", "BTC")
        btc_kraken = kraken_coins.get("Kraken", currency, "BTC")

        print(btc_gecko)
        print("")
        print(btc_binance)
        print("")
        print(btc_kraken)
        print("")

    # Persian market (Iranian Rial)
    print(f"\n\n############################")
    print(f"Currency: RLS (Iranian Rial)")
    print(f"############################")

    nobitex_coins = nobitex.fetch("RLS")
    
    if nobitex_coins.contains("Nobitex", "RLS", "BTC"):
        btc_nobitex = nobitex_coins.get("Nobitex", "RLS", "BTC")
        print(btc_nobitex)
        print("")

if __name__ == "__main__":
    main()