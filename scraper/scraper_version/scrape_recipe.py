from scraper.scraper_version.scraper_exceptions import RecipeInformationNotLoadedException, InstanceIPBlacklistedException
from scraper.scraper_version.scrape_recipe_v1 import ScrapeRecipeV1
from scraper.scraper_version.scrape_recipe_v2 import ScrapeRecipeV2

from selenium.webdriver import Chrome
from selenium import webdriver
import re
import time
import traceback

WEBDRIVER_FILE = "scraper/chromedriver.exe"
IS_HEADLESS_BROWSER = True
# On the ec2 environment, the chromedriver is set as part of the path
IS_LOCAL_CHROMEDRIVER = False
MAX_REVIEW_SCRAPE_PER_RECIPE = 400

class RecipeScrape:
    def __init__(self, recipe_link):
        self.recipe_link = recipe_link

        options = webdriver.ChromeOptions()
        if IS_HEADLESS_BROWSER:
            options.add_argument('--headless')

        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        #options.add_argument("start-maximized")                                                                                options.add_argument("enable-automation")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")

        options.add_argument("--disable-popup-blocking")

        if IS_LOCAL_CHROMEDRIVER:
            self.driver = Chrome(WEBDRIVER_FILE, options=options)
        else:
            self.driver = Chrome(options=options)

    def scrape(self):
        try: 
            self.driver.get(self.recipe_link)

            if( "<body></body>" in self.driver.page_source ):
                raise InstanceIPBlacklistedException()

            self.determine_scrape_version()
            self.scrape_version.scrape(self.driver)
        except Exception:
            raise
        finally:
            self.driver.close()

    def determine_scrape_version(self):
        # We use some random indicator on the page to determine, but may not be entirely robust; may want to find some other indicator later
        if( len(self.driver.find_elements_by_class_name("author-block")) > 0 ):
            self.scrape_version = ScrapeRecipeV1(MAX_REVIEW_SCRAPE_PER_RECIPE)
        elif( len(self.driver.find_elements_by_class_name("recipe-container-outer")) > 0 ):
            self.scrape_version = ScrapeRecipeV2(MAX_REVIEW_SCRAPE_PER_RECIPE)
        else:
            raise Exception("Invalid or unexpected version of recipe page")


if __name__ == '__main__':
    scraper = RecipeScrape("https://www.allrecipes.com/recipe/143432/black-bean-huevos-rancheros/")
    #scraper = RecipeScrape("https://www.allrecipes.com/recipe/221079/chef-johns-crab-cakes/")
    scraper.scrape()