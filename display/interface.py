from abc import ABC, abstractmethod

from graph import Graphable

class IDisplay(ABC):
    @abstractmethod
    def drawGraph(self, graph: Graphable) -> None:
        ...
