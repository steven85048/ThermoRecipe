import threading
import traceback

from scraper.recipe_model import Base, RecipeLinks, create_all
from scraper.recipe_service import RecipeService
from scraper.scraper_version.scraper_exceptions import InstanceIPBlacklistedException
from scraper.aws.invoke_lambda import invoke_abort_lambda

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

MAX_THREAD_COUNT = 2
BASE_URL = "https://www.allrecipes.com"

class RecipeBatchProcessor:
    def __init__(self):
        pass

    def reset(self):
        self.thread_link_data = None
        self.scraping_done = False

        self.needs_restart = False

    def init_engine(self, engine_url):
        self.engine = create_engine(engine_url)
        Base.metadata.bind = self.engine
        self.db_session = sessionmaker(bind=self.engine)

        create_all( self.engine )

    def scrape_on_threads(self):
        self.reset()

        active_threads = []

        cv = threading.Condition()
        for index in range(0, MAX_THREAD_COUNT):
            active_threads.append(threading.Thread(target=self.scrape_and_store_recipe_on_thread, args = (cv, )))

        for thread in active_threads:
            thread.start()

        session = self.db_session()
        links = session.query(RecipeLinks).filter(RecipeLinks.has_been_parsed == 0)

        for row in links:
            link_data = {}

            link_data["curr_link"] = BASE_URL + row.link
            link_data["link_id"] = row.id

            with cv:
                while self.thread_link_data != None and not self.needs_restart:
                    cv.wait()

                if self.needs_restart:
                    break

                self.thread_link_data = link_data
                cv.notify_all()

        self.scraping_done = True
        cv.notify_all()

        for thread in active_threads:
            thread.join()

        if( self.needs_restart ):
            invoke_abort_lambda()

    def scrape_and_store_recipe_on_thread(self, cv):
        session = self.db_session()
        recipe_service = RecipeService()

        while not self.scraping_done:
            link_data = None

            with cv:
                while self.thread_link_data == None and not self.scraping_done:
                    cv.wait()

                link_data = self.thread_link_data
                self.thread_link_data = None
                cv.notify_all()

            print("Processing url: {}".format(link_data["curr_link"]))

            if not self.scraping_done:
                try:
                    recipe_service.store_recipe(link_data["curr_link"], session)

                    # Set this link as completed
                    session.query(RecipeLinks).filter(RecipeLinks.id == link_data["link_id"])\
                                              .update({RecipeLinks.has_been_parsed: 1})

                    session.commit()
                except InstanceIPBlacklistedException as err:
                    print("We have been blacklisted; time to restart!!")
                    self.needs_restart = True
                    cv.notify_all()
                        
                except Exception as err:
                    print("Scraping on URL {} failed: {}".format(link_data["curr_link"], str(err)))    
                    traceback.print_exc()

                    # Revert the data queries for this link
                    session.rollback()

                    # Set this link as an error state
                    session.query(RecipeLinks).filter(RecipeLinks.id == link_data["link_id"])\
                                              .update({RecipeLinks.has_been_parsed: -1})

                    session.commit()

        session.close()

if __name__ == '__main__':
    batch_processor = RecipeBatchProcessor()
    batch_processor.init_engine('sqlite:///./scraper/recipe-links-sqlite.db')
    batch_processor.scrape_on_threads()