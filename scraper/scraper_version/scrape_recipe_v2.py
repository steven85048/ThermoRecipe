from scraper.scraper_version.scraper_utils import wait_until_comparison_valid

from selenium.webdriver import Chrome
from selenium.webdriver import Chrome
from selenium import webdriver

import re
import time

class ScrapeRecipeV2:
    def __init__(self, max_review_scrapes):
        self.max_review_scrapes = max_review_scrapes

    def scrape(self, driver):
        self.driver = driver

        wait_until_comparison_valid(self._get_title, "", lambda a,b : a != b, 10)

        self.scrape_title()
        self.scrape_description()
        self.scrape_ingredients()
        self.scrape_directions()
        self.scrape_reviews()

    def scrape_title(self):
        self.title = self._get_title()
        print(self.title)

    def scrape_description(self):
        self.description_text = self.driver.find_elements_by_class_name("submitter__description")[0].text

    def scrape_reviews(self):
        review_count_element = self.driver.find_elements_by_class_name("review-count")[0]
        num_reviews = int(re.findall("\d+", review_count_element.text)[0])

        review_count_element.click()

        self.reviews = []
        for rev_num in range(1, num_reviews + 1):
            if( len(self.reviews) > self.max_review_scrapes ):
                break

            # Verification/wait to handle angular loading
            WAIT_RETRIES = 10
            wait_until_comparison_valid( self._get_current_review_number, rev_num, lambda a, b : a == b, WAIT_RETRIES )

            review_store = {}

            curr_review_description = self.driver.find_elements_by_class_name("ReviewText")[0]
            review_store["description"] = curr_review_description.text

            rating_element = self.driver.find_elements_by_class_name("rating")[0]
            review_store["date"] = rating_element.text
            
            rating_stars = rating_element.get_attribute('innerHTML')
            review_store["stars"] = len(re.findall("full-star", rating_stars))/2

            review_store["helpful"] = int(self.driver.find_elements_by_css_selector(".helpful-count.reviewCount")[0].text)

            self.reviews.append(review_store)

            # Modal element selecting behaves strangely in selenium so we use the document functions instead which works better
            self.driver.execute_script("document.getElementById('BI_loadReview3_right').click()")

    def scrape_ingredients(self):
        ingredient_elements = self.driver.find_elements_by_css_selector(".recipe-ingred_txt.added")

        self.ingredients = []
        for ingredient_element in ingredient_elements:
            self.ingredients.append(ingredient_element.text)

    def scrape_directions(self):
        self.directions = []

        directions_elements = self.driver.find_elements_by_class_name("recipe-directions__list--item")
        for direction_element in directions_elements:
            self.directions.append(direction_element.text)

    def _get_title(self):
        return self.driver.find_elements_by_class_name("recipe-summary__h1")[0].text

    def _get_current_review_number(self):
        footer = self.driver.find_elements_by_css_selector(".footer.noselect")[0]
        rev_count_element = footer.find_elements_by_class_name("ng-binding")[0]
        return rev_count_element.text

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')

    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    options.add_argument("--disable-popup-blocking")

    driver = Chrome("scraper/chromedriver.exe", chrome_options=options)
    driver.get("https://www.allrecipes.com/recipe/221079/chef-johns-crab-cakes/")

    scraper = ScrapeRecipeV2()
    scraper.scrape(driver)