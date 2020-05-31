import unittest

from scraper.scraper_version.scrape_recipe import RecipeScrape

class ClientRequestTests(unittest.TestCase):
    def test_steamed_halibut(self):
        recipe = RecipeScrape("https://www.allrecipes.com/recipe/76659/heavenly-halibut/?internalSource=streams&referringId=13297&referringContentType=Recipe%20Hub&clickId=st_recipes_mades")
        recipe.scrape()
        self.assertEqual(recipe.scrape_version.title,"Heavenly Halibut")
        self.assertTrue("Rich, cheesy topping" in recipe.scrape_version.description_text)
        self.assertTrue("3 tablespoons mayonnaise" in recipe.scrape_version.ingredients)
        self.assertTrue("Preheat the oven broiler." in recipe.scrape_version.directions[0])
        self.assertTrue("This simple dish always makes" in recipe.scrape_version.reviews[0]['description'])

    def test_curry_salmon_mango(self):
        recipe = RecipeScrape("https://www.allrecipes.com/recipe/245893/curry-salmon-with-mango/?internalSource=rotd&referringContentType=Homepage")
        recipe.scrape()
        self.assertEqual(recipe.scrape_version.title,"Curry Salmon with Mango")
        self.assertTrue('"Curried salmon with mango is best served immediately. Enjoy!"' in recipe.scrape_version.description_text)
        self.assertTrue("1/4 cup avocado oil" in recipe.scrape_version.ingredients)
        self.assertTrue("Preheat oven to 400 degrees" in recipe.scrape_version.directions[0])
        self.assertTrue("Fantastic flavor!" in recipe.scrape_version.reviews[0]['description'])

    def test_black_bean_huevos_rancheros(self):
        recipe = RecipeScrape("https://www.allrecipes.com/recipe/143432/black-bean-huevos-rancheros/?internalSource=hub%20recipe&referringContentType=Search")
        recipe.scrape()
        self.assertEqual(recipe.scrape_version.title,"Black Bean Huevos Rancheros")
        self.assertTrue("Layered with black beans" in recipe.scrape_version.description_text)
        self.assertTrue("2 tablespoons fresh lime juice" in recipe.scrape_version.ingredients)
        self.assertTrue("To make the salsa" in recipe.scrape_version.directions[0])
        self.assertTrue("Absolutely delicious!" in recipe.scrape_version.reviews[0]['description'])
    
if __name__ == '__main__':
    unittest.main()