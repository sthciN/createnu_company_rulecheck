from abc import ABC, abstractmethod
from ui import UI

class RuleSetFactory(ABC):
    def __init__(self, data):
        self.data = data
        self.status = (UI.color('Risk', 'red'), UI.color('Watchful', 'yellow'), UI.color('Good Standing', 'green'))
        self.categories = ('[Company profile]', '[Financial - Legal Structure]')

    @abstractmethod
    def annotage(self):
        raise NotImplementedError("You should implement this!")

