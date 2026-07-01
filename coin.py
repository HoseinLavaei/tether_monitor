from decimal import Decimal
from typing import Any, Iterator

from pydantic import BaseModel, Field


def sort_key_with_nulls(value: Any, fallback: Any) -> tuple[int, Any]:
    """Returns a sort key tuple that places None values at the end.
    
    Used as a key function in sorted() to handle optional fields like rank and market_cap.
    """
    return value is None, value if value is not None else fallback


class Coin(BaseModel):
    """Represents a cryptocurrency with market data.
    
    Frozen model to ensure immutability after creation.
    """
    name: str
    symbol: str
    current_price: Decimal
    price_change_24h: Decimal
    high_24h: Decimal
    low_24h: Decimal
    market_cap: Decimal | None = None
    volume_24h: Decimal
    circulating_supply: Decimal | None = None
    rank: int | None = None

    model_config = {"frozen": True}

    @property
    def is_gaining(self) -> bool:
        """True if the 24h price change is positive."""
        return self.price_change_24h > 0

    @property
    def is_losing(self) -> bool:
        """True if the 24h price change is negative."""
        return self.price_change_24h < 0

    def __str__(self) -> str:
        def format_decimal(value: Decimal, decimals: int = 2) -> str:
            """Format decimal with thousands separators and specified decimal places."""
            return f"{value:,.{decimals}f}"

        lines = [
            f"Name: {self.name}",
            f"Symbol: {self.symbol}",
            f"Current Price: ${format_decimal(self.current_price)}",
            f"24h Change: {format_decimal(self.price_change_24h, 2)}%",
            f"24h High: ${format_decimal(self.high_24h)}",
            f"24h Low: ${format_decimal(self.low_24h)}",
        ]

        if self.market_cap is not None:
            lines.append(f"Market Cap: ${format_decimal(self.market_cap, 0)}")

        lines.append(f"24h Volume: ${format_decimal(self.volume_24h, 0)}")

        if self.circulating_supply is not None:
            lines.append(f"Circulating Supply: {format_decimal(self.circulating_supply, 0)}")

        if self.rank is not None:
            lines.append(f"Rank: #{self.rank}")

        return "\n".join(lines)


class Coins(BaseModel):
    """Collection of coins from a specific provider and currency.
    
    Acts as a dictionary with symbol keys for easy access.
    """
    provider: str
    currency: str
    coins: dict[str, Coin] = Field(default_factory=dict)

    @classmethod
    def from_list(cls, provider: str, currency: str, data: list[dict]) -> "Coins":
        """Create a Coins collection from a list of coin data dictionaries."""
        coins = cls(provider=provider, currency=currency)

        for coin_data in data:
            coins.upsert(Coin.model_validate(coin_data))

        return coins

    def upsert(self, coin: Coin) -> None:
        """Add or update a coin in the collection."""
        self.coins[coin.symbol] = coin

    def remove(self, symbol: str) -> None:
        """Remove a coin from the collection by symbol."""
        del self.coins[symbol.upper()]


    def sorted_by_rank(self) -> list[Coin]:
        """Return coins sorted by rank (ascending), with None values last."""
        return sorted(
            self,
            key=lambda c: sort_key_with_nulls(c.rank, 0)
        )

    def sorted_by_market_cap(self) -> list[Coin]:
        """Return coins sorted by market cap (descending), with None values last."""
        return sorted(
            self,
            key=lambda c: sort_key_with_nulls(c.market_cap, Decimal(0)),
            reverse=True
        )

    def __contains__(self, symbol: str) -> bool:
        """Check if a coin symbol exists in the collection."""
        return symbol.upper() in self.coins

    def __len__(self) -> int:
        """Return the number of coins in the collection."""
        return len(self.coins)

    def __iter__(self) -> Iterator[Coin]:
        """Iterate over all coins in the collection."""
        return iter(self.coins.values())

    def __getitem__(self, symbol: str) -> Coin:
        """Get a coin by symbol using bracket notation (coins['BTC'])."""
        return self.coins[symbol.upper()]

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
