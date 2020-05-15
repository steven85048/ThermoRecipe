import threading

from scraper.recipe_model import Base, RecipeLinks, create_all
from scraper.recipe_service import RecipeService

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

MAX_THREAD_COUNT = 2
BASE_URL = "https://www.allrecipes.com"

class RecipeBatchProcessor:
    def __init__(self):
        pass

    def reset(self):
        self.thread_url = None
        self.scraping_done = False

    def init_engine(self, engine_url):
        self.engine = create_engine(engine_url)
        Base.metadata.bind = self.engine
        self.db_session = sessionmaker(bind=self.engine)

        create_all( self.engine )

        self.recipe_service = RecipeService()

    def scrape_on_threads(self):
        self.reset()

        active_threads = []

        cv = threading.Condition()
        for index in range(0, MAX_THREAD_COUNT):
            active_threads.append(threading.Thread(target=self.scrape_and_store_recipe_on_thread, args = (cv, )))

        for thread in active_threads:
            thread.start()

        session = self.db_session()
        links = session.query(RecipeLinks).all()

        for row in links:
            curr_link = BASE_URL + row.link

            with cv:
                while self.thread_url != None:
                    cv.wait()

                self.thread_url = curr_link
                cv.notify_all()

        self.scraping_done = True
        cv.notify_all()

    def scrape_and_store_recipe_on_thread(self, cv):
        session = self.db_session()

        while not self.scraping_done:
            curr_url = None

            with cv:
                while self.thread_url == None and not self.scraping_done:
                    cv.wait()

                curr_url = self.thread_url
                self.thread_url = None
                cv.notify_all()

            print("Processing url: {}".format(curr_url))

            if not self.scraping_done:
                self.recipe_service.store_recipe(curr_url, session)
        
        session.close()

if __name__ == '__main__':
    batch_processor = RecipeBatchProcessor()
    batch_processor.init_engine('sqlite:///./scraper/recipe-links-sqlite.db')
    batch_processor.scrape_on_threads()