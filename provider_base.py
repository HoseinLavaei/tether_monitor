from abc import ABC, abstractmethod

from coin import Coins


class Provider(ABC):
    """Abstract base class for cryptocurrency data providers.
    
    All providers must implement the fetch method to retrieve coin data.
    """
    name: str

    @abstractmethod
    def fetch(self, currency: str) -> Coins:
        """Fetch coin data for a given currency from the provider's API."""
        pass