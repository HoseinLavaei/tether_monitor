from providers.nobitex import NobitexProvider
from providers.aban_tether import AbanTetherProvider
from providers.bitpin import BitpinProvider
from providers.wallex import WallexProvider
from providers.ramzinex import RamzinexProvider
from providers.exir import ExirProvider

def main():
    nobitex = NobitexProvider()
    aban_tether = AbanTetherProvider()
    bitpin = BitpinProvider()
    wallex = WallexProvider()
    ramzinex = RamzinexProvider()
    exir = ExirProvider()

    print(f"############################")
    print(f"Currency: RLS (Iranian Rial)")
    print(f"############################")

    nobitex_coins = nobitex.fetch("RLS")
    aban_tether_coins = aban_tether.fetch("IRT")
    bitpin_coins = bitpin.fetch("IRT")
    wallex_coins = wallex.fetch("TMN")
    ramzinex_coins = ramzinex.fetch("irr")
    exir_coins = exir.fetch("IRT")

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

    if ramzinex_coins.contains("Ramzinex", "irr", "btc"):
        btc_ramzinex = ramzinex_coins.get("Ramzinex", "irr", "btc")
        print(btc_ramzinex)
        print("")

    if exir_coins.contains("Exir", "IRT", "BTC"):
        btc_exir = exir_coins.get("Exir", "IRT", "BTC")
        print(btc_exir)
        print("")


if __name__ == "__main__":
    main()