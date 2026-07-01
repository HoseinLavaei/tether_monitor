from providers.coingecko import CoinGeckoProvider
from providers.biance import BinanceProvider

def print_coin(source: str, coin):
    print(f"\n===== {source} =====")
    print(coin)


def main():
    gecko = CoinGeckoProvider()
    binance = BinanceProvider()

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

        btc_gecko = gecko_coins.get("BTC")
        btc_binance = binance_coins.get("BTC")

        print_coin(f"CoinGecko BTC/{currency}", btc_gecko)
        print_coin("Binance BTC/USDT", btc_binance)


if __name__ == "__main__":
    main()