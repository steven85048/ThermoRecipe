from selenium.webdriver import Chrome

import re
import time

WEBDRIVER_FILE = "./chromedriver.exe"

class RecipeScrape:
    def __init__(self, recipe_link):
        self.recipe_link = recipe_link
        self.driver = Chrome(WEBDRIVER_FILE)
        self.driver.get(self.recipe_link)

    def scrape(self):
        self.scrape_title()
        self.scrape_description()
        self.scrape_ingredients()
        self.scrape_directions()
        self.scrape_reviews()

    def scrape_title(self):
        self.title = self.driver.find_elements_by_class_name("recipe-summary__h1")[0].text

    def scrape_description(self):
        self.description_text = self.driver.find_elements_by_class_name("submitter__description")[0].text

    def scrape_reviews(self):
        review_count_element = self.driver.find_elements_by_class_name("review-count")[0]
        num_reviews = int(re.findall("\d+", review_count_element.text)[0])

        review_count_element.click()

        self.reviews = []
        for rev_num in range(1, num_reviews + 1):
            # Verification/wait to handle angular loading
            WAIT_RETRIES = 20
            self._wait_until_func_changes_to_val( self._get_current_review_number, rev_num, WAIT_RETRIES )

            review_store = {}

            curr_review_description = self.driver.find_elements_by_class_name("ReviewText")[0]
            review_store["description"] = curr_review_description.text

            rating_element = self.driver.find_elements_by_class_name("rating")[0]
            review_store["date"] = rating_element.text
            
            rating_stars = rating_element.get_attribute('innerHTML')
            review_store["stars"] = len(re.findall("full-star", rating_stars))/2

            review_store["helpful"] = int(self.driver.find_elements_by_css_selector(".helpful-count.reviewCount")[0].text)

            print(review_store)
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

    def _get_current_review_number(self):
        footer = self.driver.find_elements_by_css_selector(".footer.noselect")[0]
        rev_count_element = footer.find_elements_by_class_name("ng-binding")[0]
        return rev_count_element.text

    def _wait_until_func_changes_to_val(self, func, val, max_retries, curr_retries = 0):
        RETRY_RATE = .5 # in seconds

        if(curr_retries >= max_retries):
            raise Exception("Error in HTML state: value of element did not change to {}".format(str(val)))
        curr_retries += 1

        time.sleep(RETRY_RATE)

        try:
            func_val = func()
            if( func_val == str(val) ):
                return
        except Exception as err:
            # we prioritize retries since errors are most likely due to timing
            print(err)
 
        self._wait_until_func_changes_to_val(func, val, max_retries, curr_retries)

if __name__ == '__main__':
    scraper = RecipeScrape("https://www.allrecipes.com/recipe/221079/chef-johns-crab-cakes/")
    scraper.scrape_directions()