from abc import ABC, abstractmethod
from coin import Coins


class Provider(ABC):
    name: str

    @abstractmethod
    def fetch(self, currency: str) -> Coins:
        pass