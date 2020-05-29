from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)

    title = Column(String(250))
    recipe_note = Column(String(1000))
    url = Column(String(100))

class Ingredients(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)

    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    recipe = relationship(Recipe, foreign_keys=[recipe_id])
    
    ingredient = Column(String(150), nullable=False)

class Directions(Base):
    __tablename__ = 'directions'

    id = Column(Integer, primary_key=True)

    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    recipe = relationship(Recipe, foreign_keys=[recipe_id])
    
    order = Column(Integer, nullable = False)
    direction = Column(String(350), nullable = False)

class Reviews(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)

    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    recipe = relationship(Recipe, foreign_keys=[recipe_id])
    
    date = Column(DateTime, default=datetime.datetime.utcnow)
    stars = Column(Integer)
    helpful = Column(Integer)
    description = Column(String(1000))

class RecipeLinks(Base):
    __tablename__ = 'recipe_links'

    id = Column(Integer, primary_key=True)
    link = Column(String(5000), nullable=False, unique=True)
    has_been_parsed = Column(Integer)

def create_all(engine):
    Base.metadata.create_all(engine)

def drop_all(engine):
    Base.metadata.drop_all(engine)

if __name__ == '__main__':
    engine = create_engine('sqlite:///./recipe-links-sqlite.db')
    create_all(engine)