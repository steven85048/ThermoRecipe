import time
import os
import sys

import pandas as pd
from sqlalchemy import create_engine

def load_from_db():
    try:
        connection_url = os.environ["RDS_SCRAPER_URL"]
    except KeyError:
        print("Error: RDS_SCRAPER_URL Not Set")
        sys.exit(1)

    engine = create_engine(connection_url, execution_options=dict(stream_results=True), server_side_cursors=True)

    df = pd.read_sql_table('reviews', engine, chunksize=5000)

    for data in df:
        yield data

def load_from_subset_pickle():
    SUBSET_PICKLE_PATH = "./model/subset.pkl"
    df = pd.read_pickle(SUBSET_PICKLE_PATH)
    return df