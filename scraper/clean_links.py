from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from scraper.recipe_model import RecipeLinks

import logging
import re

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_engine('sqlite:///./scraper/recipe-links-sqlite.db')

Base = declarative_base()

class RecipeLinks(Base):
    __tablename__ = 'recipe_links'

    id = Column(Integer, primary_key=True)
    link = Column(String(5000), nullable=False, unique=True)

Base.metadata.bind = engine
Base.metadata.create_all()

db_session = sessionmaker(bind=engine) 
session = db_session()

res = session.query(RecipeLinks).all()
print("The links are {}".format(res))

for row in res:
    filtered_link = re.sub("(photos|reviews|print|fullrecipenutrition).*", "", row.link) 
    if(filtered_link != row.link):
        print("Deleting: {}".format(row.link))
        session.query(RecipeLinks).filter(RecipeLinks.id == row.id).delete()

    if(session.query(RecipeLinks).filter(RecipeLinks.link == filtered_link) == None):
        new_recipe = RecipeLinks(link=filtered_link)
        RecipeLinks.add(new_recipe)

session.commit()