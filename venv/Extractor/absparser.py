from abc import ABC, abstractmethod  # abc is a built-in class that has obvious name

class AbsParser(ABC):
    """Abstract class for Data Extractor"""

    @abstractmethod
    def process(self):
        """ extract data from specific source  """
