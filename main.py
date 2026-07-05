from providers.coingecko import CoinGeckoProvider
from providers.binance import BinanceProvider
from providers.kraken import KrakenProvider
from providers.nobitex import NobitexProvider
from providers.aban_tether import AbanTetherProvider
from providers.bitpin import BitpinProvider
from providers.wallex import WallexProvider

def main():
    gecko = CoinGeckoProvider()
    binance = BinanceProvider()
    kraken = KrakenProvider()
    nobitex = NobitexProvider()
    aban_tether = AbanTetherProvider()
    bitpin = BitpinProvider()
    wallex = WallexProvider()

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
    aban_tether_coins = aban_tether.fetch("IRT")
    bitpin_coins = bitpin.fetch("IRT")
    wallex_coins = wallex.fetch("TMN")


    if nobitex_coins.contains("Nobitex", "RLS", "BTC"):
        btc_nobitex = nobitex_coins.get("Nobitex", "RLS", "BTC")
        print(btc_nobitex)
        print("")

    if aban_tether_coins.contains("AbanTether", "IRT", "BTC"):
        btc_aban_tether = aban_tether_coins.get("AbanTether", "IRT", "BTC")
        print(btc_aban_tether)
        print("")

    if bitpin_coins.contains("Bitpin", "IRT", "BTC"):
        btc_bitpin = bitpin_coins.get("Bitpin", "IRT", "BTC")
        print(btc_bitpin)
        print("")


    if wallex_coins.contains("Wallex", "TMN", "BTC"):
        btc_wallex = wallex_coins.get("Wallex", "TMN", "BTC")
        print(btc_wallex)
        print("")


if __name__ == "__main__":
    main()


from providers.wallex import WallexProvider