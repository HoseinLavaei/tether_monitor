from providers.coingecko import CoinGeckoProvider
from providers.binance import BinanceProvider
from providers.kraken import KrakenProvider
from providers.nobitex import NobitexProvider

def print_coin(source: str, coin):
    print(f"\n===== {source} =====")
    print(coin)


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

        btc_gecko = gecko_coins["BTC"]
        btc_binance = binance_coins["BTC"]
        btc_kraken = kraken_coins["BTC"]

        print_coin(f"CoinGecko BTC/{currency}", btc_gecko)
        print_coin("Binance BTC/USDT", btc_binance)
        print_coin(f"Kraken BTC/{currency}", btc_kraken)

    # Persian market (Iranian Rial)
    print(f"\n\n############################")
    print(f"Currency: RLS (Iranian Rial)")
    print(f"############################")

    nobitex_coins = nobitex.fetch("RLS")
    
    if "BTC" in nobitex_coins:
        btc_nobitex = nobitex_coins["BTC"]
        print_coin("Nobitex BTC/RLS", btc_nobitex)


if __name__ == "__main__":
    main()