from abc import ABC, abstractmethod


class Brakes(ABC):
    @abstractmethod
    def brake(self):
        pass
