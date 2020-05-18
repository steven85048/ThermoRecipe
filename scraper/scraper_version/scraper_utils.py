from scraper.scraper_version.scraper_exceptions import RecipeInformationNotLoadedException

import time

# Having self is strange in a utility function here, but we just use it to pass into our func as convenience
def wait_until_comparison_valid(func, val, comparison, max_retries, curr_retries = 0):
    RETRY_RATE = .5 # in seconds

    if(curr_retries >= max_retries):
        raise RecipeInformationNotLoadedException("Error in HTML state: value of element did not change to {}".format(str(val)))
    curr_retries += 1

    time.sleep(RETRY_RATE)

    try:
        func_val = func()
        if( comparison(func_val, str(val))):
            return
    except Exception as err:
        # we prioritize retries since we care about errors due to timing
        print(err)
        pass

    wait_until_comparison_valid(func, val, comparison, max_retries, curr_retries)