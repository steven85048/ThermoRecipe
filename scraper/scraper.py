import os

from scraper.recipe_batch_processor import RecipeBatchProcessor

def scrape_with_rds():
    try:
        connection_url = os.environ["RDS_SCRAPER_URL"]
    except KeyError:
        print("Error: RDS_SCRAPER_URL Not Set")
        sys.exit(1)

    batch_processor = RecipeBatchProcessor()
    batch_processor.init_engine(connection_url)
    batch_processor.scrape_on_threads()

def scrape_with_sqlite():
    batch_processor = RecipeBatchProcessor()
    batch_processor.init_engine('sqlite:///./scraper/recipe-links-sqlite.db')
    batch_processor.scrape_on_threads()