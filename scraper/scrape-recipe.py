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
        self.scrape_description()
        self.scrape_reviews()

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

            curr_review = self.driver.find_elements_by_class_name("ReviewText")[0]
            self.reviews.append(curr_review.text)

            self.driver.execute_script("document.getElementById('BI_loadReview3_right').click()")

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
    scraper.scrape()