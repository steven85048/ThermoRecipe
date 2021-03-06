from datetime import datetime

from scraper.recipe_model import Base, Ingredients, Recipe, Reviews, Directions, create_all, drop_all
from scraper.recipe_model import RECIPE_NOTE_MAX_LEN, INGREDIENT_MAX_LEN, DIRECTION_MAX_LEN, REVIEW_MAX_LEN
from scraper.scraper_version.scrape_recipe import RecipeScrape

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging

SHOULD_LOG_QUERIES = False

class RecipeService:
    def __init__(self):
        if(SHOULD_LOG_QUERIES):
            logging.basicConfig()
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    def store_recipe(self, recipe_link, session):
        self.scraper = RecipeScrape(recipe_link)
        self.scraper.scrape()

        recipe = self._store_recipe(session)
        self._store_ingredients(session, recipe)
        self._store_directions(session, recipe)
        self._store_reviews(session, recipe)

    def _store_recipe(self, session):
        new_recipe = Recipe(title=self.scraper.scrape_version.title, recipe_note=self.scraper.scrape_version.description_text[:RECIPE_NOTE_MAX_LEN], url=self.scraper.recipe_link)
        session.add(new_recipe)

        # Need to flush session changes to get the ID of the recipe for foreign key purposes
        session.flush()
        return new_recipe

    def _store_ingredients(self, session, recipe):
        for ingredient in self.scraper.scrape_version.ingredients:
            new_ingredient = Ingredients(recipe=recipe, 
                                         ingredient=ingredient[:INGREDIENT_MAX_LEN])
            session.add(new_ingredient)

    def _store_directions(self, session, recipe):
        for index, direction in enumerate(self.scraper.scrape_version.directions):
            new_direction = Directions( recipe=recipe, 
                                        order=index, 
                                        direction=direction[:DIRECTION_MAX_LEN])
            session.add(new_direction)

    def _store_reviews(self, session, recipe):
        storeable_reviews = [self._to_storeable_review(r, recipe) for r in self.scraper.scrape_version.reviews]
        for review in storeable_reviews:
            session.add(review)

    def _to_storeable_review(self, review, recipe):
        
        parsed_date = None
        date_formats = ["%B %d, %Y", "%m/%d/%Y"]
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(review["date"], date_format)
            except Exception as err:
                pass

        new_review = Reviews(recipe=recipe, 
                            date=parsed_date, 
                            stars=review['stars'], 
                            description=review["description"][:REVIEW_MAX_LEN], 
                            helpful=review["helpful"])
        return new_review

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    engine = create_engine('sqlite:///./recipe-links-sqlite.db')
    drop_all(engine)
    create_all(engine)

    Base.metadata.bind = engine
    db_session = sessionmaker(bind=engine) 
    session = db_session()

    recipe_service = RecipeService()
    recipe_service.store_recipe("https://www.allrecipes.com/recipe/228542/roasted-vegetables-with-spaghetti-squash/", session)