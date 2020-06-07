import time
import os
import sys

import pandas as pd
from sqlalchemy import create_engine

def _connect_to_psql():
    try:
        connection_url = os.environ["RDS_SCRAPER_URL"]
    except KeyError:
        print("Error: RDS_SCRAPER_URL Not Set")
        sys.exit(1)

    engine = create_engine(connection_url, execution_options=dict(stream_results=True), server_side_cursors=True)
    return engine

def load_from_db():
    engine = _connect_to_psql()

    df = pd.read_sql_table('reviews', engine, chunksize=5000)
    df = pd.query('')

    for data in df:
        yield data

def load_id_range(min, max):
    engine = _connect_to_psql()

    recipe_df = pd.read_sql("SELECT * FROM recipes WHERE id > {} AND id < {};".format(min, max), 
                             con=engine)

    reviews_df = pd.read_sql("SELECT * FROM reviews WHERE recipe_id > {} AND recipe_id < {};".format(min,max),
                             con=engine)

    ingredients_df = pd.read_sql("SELECT * FROM ingredients WHERE recipe_id > {} AND recipe_id < {};".format(min,max),
                             con=engine)

    return recipe_df, reviews_df, ingredients_df

def load_from_subset_pickle():
    SUBSET_PICKLE_PATH = "./model/subset.pkl"
    df = pd.read_pickle(SUBSET_PICKLE_PATH)
    return df
