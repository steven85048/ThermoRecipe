from abc import ABC, abstractmethod

class ScrapeRecipeInterface(ABC):
    @abstractmethod
    def scrape(self, driver, url):
        pass