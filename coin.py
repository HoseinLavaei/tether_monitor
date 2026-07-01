from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Iterator, Mapping, Self


def nulls_last(value: Any, fallback: Any) -> tuple[int, Any]:
    """
    Sorting helper: puts None values at the end.
    """
    return value is None, value if value is not None else fallback


# ----------------------------
# Coin
# ----------------------------

@dataclass(slots=True, frozen=True)
class Coin:
    name: str
    symbol: str
    current_price: Decimal
    price_change_24h: Decimal
    high_24h: Decimal
    low_24h: Decimal
    market_cap: Decimal | None
    volume_24h: Decimal
    circulating_supply: Decimal | None
    rank: int | None

    @classmethod
    def from_string(cls, data: str) -> Self:
        slices = [s.strip() for s in data.split(",")]

        if len(slices) != 10:
            raise ValueError(
                f"Expected 10 comma-separated values, got {len(slices)}."
            )

        def dec(x: str) -> Decimal | None:
            return Decimal(x) if x not in ("", "None", None) else None

        def integer(x: str) -> int | None:
            return int(x) if x not in ("", "None", None) else None

        return cls(
            name=slices[0],
            symbol=slices[1].upper(),
            current_price=Decimal(slices[2]),
            price_change_24h=Decimal(slices[3]),
            high_24h=Decimal(slices[4]),
            low_24h=Decimal(slices[5]),
            market_cap=dec(slices[6]),
            volume_24h=Decimal(slices[7]),
            circulating_supply=dec(slices[8]),
            rank=integer(slices[9]),
        )

    @classmethod
    def parse(cls, data: str | Mapping[str, Any]) -> Self:
        if isinstance(data, str):
            return cls.from_string(data)
        if isinstance(data, Mapping):
            return cls(**data)

        raise TypeError(f"Unsupported type: {type(data).__name__}")

    @property
    def is_gaining(self) -> bool:
        return self.price_change_24h > 0

    @property
    def is_losing(self) -> bool:
        return self.price_change_24h < 0

    def __str__(self) -> str:
        lines = [
            f"Name: {self.name}",
            f"Symbol: {self.symbol}",
            f"Current Price: {self.current_price}",
            f"24h Change: {self.price_change_24h}%",
            f"24h High: {self.high_24h}",
            f"24h Low: {self.low_24h}",
        ]

        if self.market_cap is not None:
            lines.append(f"Market Cap: {self.market_cap}")

        lines.append(f"24h Volume: {self.volume_24h}")

        if self.circulating_supply is not None:
            lines.append(f"Circulating Supply: {self.circulating_supply}")

        if self.rank is not None:
            lines.append(f"Rank: #{self.rank}")

        return "\n".join(lines)


# ----------------------------
# Coins collection
# ----------------------------

@dataclass(slots=True)
class Coins:
    provider: str
    currency: str
    coins: dict[str, Coin] = field(default_factory=dict)

    @classmethod
    def from_string(cls, provider: str, currency: str, data: str) -> Self:
        coins = cls(provider, currency)

        for coin_data in data.split("|"):
            coin_data = coin_data.strip()
            if coin_data:
                coins.add(Coin.parse(coin_data))

        return coins

    @classmethod
    def from_list(cls, provider: str, currency: str, data: list[Mapping[str, Any] | str]) -> Self:
        coins = cls(provider, currency)

        for coin_data in data:
            coins.add(Coin.parse(coin_data))

        return coins

    def add(self, coin: Coin) -> None:
        if coin.symbol in self:
            raise ValueError(f"{coin.symbol} already exists.")

        self.coins[coin.symbol] = coin

    def update(self, coin: Coin) -> None:
        if coin.symbol not in self:
            raise KeyError(f"{coin.symbol} does not exist.")

        self.coins[coin.symbol] = coin

    def remove(self, symbol: str) -> None:
        del self.coins[symbol.upper()]

    def get(self, symbol: str) -> Coin:
        return self.coins[symbol.upper()]

    # ----------------------------
    # Sorting (null-safe)
    # ----------------------------

    def sorted_by_rank(self) -> list[Coin]:
        return sorted(
            self,
            key=lambda c: nulls_last(c.rank, 0)
        )

    def sorted_by_market_cap(self) -> list[Coin]:
        return sorted(
            self,
            key=lambda c: nulls_last(c.market_cap, Decimal(0)),
            reverse=True
        )

    # ----------------------------
    # Dunder methods
    # ----------------------------

    def __contains__(self, symbol: str) -> bool:
        return symbol.upper() in self.coins

    def __len__(self) -> int:
        return len(self.coins)

    def __iter__(self) -> Iterator[Coin]:
        return iter(self.coins.values())

    def __getitem__(self, symbol: str) -> Coin:
        return self.get(symbol)

    def __str__(self) -> str:
        if not self.coins:
            return (
                f"Provider: {self.provider}\n"
                f"Currency: {self.currency}\n"
                f"(No coins)"
            )

        return (
                f"Provider: {self.provider}\n"
                f"Currency: {self.currency}\n"
                f"Number of coins: {len(self)}\n\n"
                + "\n\n".join(str(coin) for coin in self)
        )
