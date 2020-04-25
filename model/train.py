import sqlite3
import pandas as pd
import numpy as np
import nltk
import string
import re

con = sqlite3.connect("./database.sqlite")
df = pd.read_sql_query("SELECT * FROM Reviews;", con)