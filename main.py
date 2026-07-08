from providers.nobitex import NobitexProvider
from providers.aban_tether import AbanTetherProvider
from providers.bitpin import BitpinProvider
from providers.wallex import WallexProvider

def main():
    nobitex = NobitexProvider()
    aban_tether = AbanTetherProvider()
    bitpin = BitpinProvider()
    wallex = WallexProvider()

    print(f"############################")
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