from abc import ABC, abstractmethod
from ui import UI

class RuleSetFactory(ABC):
    def __init__(self, data, verbose):
        self.data = data
        self._verbose = verbose
        self.status = (UI.color('Risk', 'red'), UI.color('Watchful', 'yellow'), UI.color('Good Standing', 'green'))
        self.categories = ('[Company profile]', '[Financial - Legal Structure]')
    
    def empty_annotation_info(self):
        return ['']*2 if not self._verbose else ['']*4

    @abstractmethod
    def annotage(self):
        raise NotImplementedError("You should implement this!")

