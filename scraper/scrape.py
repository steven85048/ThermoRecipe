import scrapy

class AllRecipeScraper(scrapy.Spider):
    name = "all_recipe_scraper"
    start_urls = ['https://www.allrecipes.com/']
