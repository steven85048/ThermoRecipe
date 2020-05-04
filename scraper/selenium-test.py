from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time

import re

webdriver = './chromedriver.exe'
driver = Chrome(webdriver)

url = "https://www.allrecipes.com/recipe/221079/chef-johns-crab-cakes/"

driver.get(url)

description = driver.find_elements_by_class_name("submitter__description")[0]
print(description.text)

review_count = driver.find_elements_by_class_name("review-count")[0]
num_reviews = int(re.findall("\d+", review_count.text)[0])
print(num_reviews)
review_count.click()
for rev_num in range(0, num_reviews):
    review = driver.find_elements_by_class_name("ReviewText")[0]
    print(review.text)    

    driver.execute_script("document.getElementById('BI_loadReview3_right').click()")

    def wait_until_js_val_changes(driver, val, max_retries, curr_retries = 0):
        RETRY_RATE = .5 # in seconds        

        if(curr_retries >= max_retries):
            raise Exception("JS value never changed")
        curr_retries += 1

        time.sleep(RETRY_RATE)

        try:
            footer = driver.find_elements_by_css_selector(".footer.noselect")[0]
            rev_count_element = footer.find_elements_by_class_name("ng-binding")[0]
        except Exception as err:
            print(err)
            wait_until_js_val_changes(driver, val, max_retries, curr_retries)
            pass

        # TODO: catch selenium.common.exceptions.JavascriptException
        curr_rev_index = rev_count_element.text
        if(curr_rev_index == str(val)):
            wait_until_js_val_changes(driver, val, max_retries, curr_retries)

    wait_until_js_val_changes(driver, rev_num, 20)

driver.close() 