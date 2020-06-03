import os
import sys

import pandas as pd
from sqlalchemy import create_engine

try:
    connection_url = os.environ["RDS_SCRAPER_URL"]
except KeyError:
    print("Error: RDS_SCRAPER_URL Not Set")
    sys.exit(1)

engine = create_engine(connection_url)
df = pd.read_sql_table('reviews', engine)

print(df.head(5))