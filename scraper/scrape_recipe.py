from selenium.webdriver import Chrome

import re
import time
import traceback

WEBDRIVER_FILE = "scraper/chromedriver.exe"

class RecipeScrape:
    def __init__(self, recipe_link):
        self.recipe_link = recipe_link
        self.driver = Chrome(WEBDRIVER_FILE)
        self.driver.get(self.recipe_link)

    def scrape(self):
        self._wait_until_func_changes_to_val(self._get_title, "", lambda a,b : a != b, 10)

        self.scrape_title()
        self.scrape_description()
        self.scrape_ingredients()
        self.scrape_directions()
        self.scrape_reviews()

    # Used for validation of page loaded
    def _get_title(self):
        return self.driver.find_elements_by_css_selector(".headline-wrapper")[0].text

    def scrape_title(self):
        self.title = self._get_title()

    def scrape_description(self):
        self.description_text = self.driver.find_elements_by_class_name("recipe-summary")[0].text

    def scrape_reviews(self):
        review_count_element = self.driver.find_elements_by_css_selector(".ugc-reviews-link")[1]        
        num_reviews = int(re.findall("\d+", review_count_element.text)[0])

        review_count_element.click()

        self.reviews = []
        for rev_num in range(1, num_reviews + 1):
            # Verification/wait to handle angular loading
            WAIT_RETRIES = 20
            self._wait_until_func_changes_to_val( self._get_current_review_number, rev_num, lambda a, b : a == b, WAIT_RETRIES )

            review_store = {}

            active_review_element = self.driver.find_elements_by_css_selector(".owl-item.active.center")[0]

            curr_review_description = active_review_element.find_elements_by_class_name("recipe-review-body")[0]
            review_store["description"] = curr_review_description.text

            review_store["date"] = active_review_element.find_elements_by_css_selector('.recipe-review-date')[0].text
            review_store["stars"] = len(active_review_element.find_elements_by_css_selector('.rating-star.active'))
            
            try:
                helpful = active_review_element.find_elements_by_css_selector(".recipe-review-helpful-count")[0].text
                review_store["helpful"] = int(re.sub('[^0-9]','', helpful))
            except IndexError:
                review_store["helpful"] = 0

            self.reviews.append(review_store)

            # Modal element selecting behaves strangely in selenium so we use the document functions instead which works better
            self.driver.execute_script("document.getElementsByClassName('ugc-review-next')[0].click()")

    def scrape_ingredients(self):
        ingredient_elements = self.driver.find_elements_by_css_selector(".ingredients-item-name")

        self.ingredients = []
        for ingredient_element in ingredient_elements:
            self.ingredients.append(ingredient_element.text)

    def scrape_directions(self):
        self.directions = []

        directions_section_element = self.driver.find_elements_by_class_name("instructions-section")[0]
        directions_elements = directions_section_element.find_elements_by_class_name("section-body")
        for direction_element in directions_elements:
            self.directions.append(direction_element.text)

    def _get_current_review_number(self):
        index_element = self.driver.find_elements_by_css_selector(".review-index")[0]
        return index_element.text

    def _wait_until_func_changes_to_val(self, func, val, comparison, max_retries, curr_retries = 0):
        RETRY_RATE = .5 # in seconds

        if(curr_retries >= max_retries):
            raise Exception("Error in HTML state: value of element did not change to {}".format(str(val)))
        curr_retries += 1

        time.sleep(RETRY_RATE)

        try:
            func_val = func()
            if( comparison(func_val, str(val))):
                return
        except Exception as err:
            # we prioritize retries since errors are most likely due to timing
            traceback.print_exc()
 
        self._wait_until_func_changes_to_val(func, val, max_retries, curr_retries)

if __name__ == '__main__':
    scraper = RecipeScrape("https://www.allrecipes.com/recipe/228542/roasted-vegetables-with-spaghetti-squash/")
    scraper.scrape_title()