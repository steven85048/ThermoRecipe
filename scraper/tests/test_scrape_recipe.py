import unittest

from scraper.scrape_recipe import RecipeScrape

class ClientRequestTests(unittest.TestCase):
    def test_steamed_halibut(self):
        recipe = RecipeScrape("https://www.allrecipes.com/recipe/76659/heavenly-halibut/?internalSource=streams&referringId=13297&referringContentType=Recipe%20Hub&clickId=st_recipes_mades")
        recipe.scrape_title()
        self.assertEqual(recipe.title,"Heavenly Halibut")

    def test_curry_salmon_mango(self):
        recipe = RecipeScrape("https://www.allrecipes.com/recipe/245893/curry-salmon-with-mango/?internalSource=rotd&referringContentType=Homepage")
        recipe.scrape_title()
        self.assertEqual(recipe.title,"Curry Salmon with Mango")

    def test_black_bean_huevos_rancheros(self):
        recipe = RecipeScrape("https://www.allrecipes.com/recipe/143432/black-bean-huevos-rancheros/?internalSource=hub%20recipe&referringContentType=Search")
        recipe.scrape_title()
        self.assertEqual(recipe.title,"Black Bean Huevos Rancheros")
    
if __name__ == '__main__':
    unittest.main()