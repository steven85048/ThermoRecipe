import threading

from scraper.recipe_model import Base
from scraper.recipe_service import RecipeService

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

MAX_THREAD_COUNT = 5

class RecipeBatchProcessor:
    def __init__(self):
        pass

    def init_engine(self, engine_url):
        self.engine = create_engine(engine_url)
        Base.metadata.bind = self.engine
        self.db_session = sessionmaker(bind=self.engine)

        self.recipe_service = RecipeService()

    def scrape_on_threads(self):
        global thread_url
        global scraping_done

        active_threads = []

        cv = threading.Condition()
        for index in range(0, MAX_THREAD_COUNT):
            active_threads.append(threading.Thread(target=self.scrape_and_store_recipe, args = (cv, )))

        for thread in active_threads:
            thread.start()

        

    def scrape_and_store_recipe(self, recipe_link):
        session = self.db_session()
        self.recipe_service.store_recipe(recipe_link, session)
        session.close()

if __name__ == '__main__':
    batch_processor = RecipeBatchProcessor()
    batch_processor.init_engine('sqlite:///./recipe-links-sqlite.db')
    batch_processor.scrape_and_store_recipe("https://www.allrecipes.com/recipe/228542/roasted-vegetables-with-spaghetti-squash/")