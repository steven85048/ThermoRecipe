import requests
import re
import sqlite3
import sys
from sqlite3 import Error, IntegrityError

CRAWL_WRITE_FILE = 'recipe-links-sqlite.db'
BASE_LINK = 'https://www.allrecipes.com'
ROUTE_LINK_INITIAL = '/recipes/78/breakfast-and-brunch/'
CRAWL_MAX = 5000

class SqliteManager:
	def __init__(self, sqlite_file):
		try:
			self.conn = sqlite3.connect(CRAWL_WRITE_FILE)
			self._create_links_table()
		except Error as e:
			print(e)
			sys.exit()

	def insert_new_link(self, link):
		try:
			sql_insert_link = """ INSERT INTO recipe_links( link )
										VALUES(?); """

			self._execute_query_with_params( sql_insert_link, (link,) )
		except IntegrityError as err:
			# Ignore uniqueness constraints since we are using it as a hashset
			pass
		except Exception as err:
			print(err)

	def _create_links_table(self):
		sql_create_links_table = """ CREATE TABLE IF NOT EXISTS recipe_links (
										id INTEGER PRIMARY KEY AUTOINCREMENT,
										link CHAR(500) NOT NULL UNIQUE
								); """
	
		self._execute_query( sql_create_links_table )

	def _execute_query_with_params(self, query, params):
		try:
			c = self.conn.cursor()
			c.execute( query, params )
			self.conn.commit()
		except Exception:
			raise

	def _execute_query(self, query):
		try: 
			c = self.conn.cursor()
			c.execute( query )
			self.conn.commit()
		except Exception:
			raise

def scrape( queue, seen_links, link, sqlite_manager ):
	if link in seen_links:
		return

	seen_links.add(link)

	try:
		response = requests.get(BASE_LINK + curr_link)
		parsed_links = re.findall("(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", response.text)

		for link in parsed_links:
			route_info = link[2]

			# clean all extraneous parts of the URL
			route_info = route_info.split('%')[0]
			route_info = route_info.split('link?')[0]
			route_info = route_info.split('?')[0]

			if link[1] == u'www.allrecipes.com' and '/recipe/' in route_info:
				queue.append(route_info)
				sqlite_manager.insert_new_link(route_info)

	except Exception as e:
		print(e)
		raise

queue = []
queue.append(ROUTE_LINK_INITIAL)
seen_links = set()

sqlite_manager = SqliteManager(CRAWL_WRITE_FILE)

crawl_counter = 0

while len(queue) != 0: 
	if crawl_counter > CRAWL_MAX:
		break

	curr_link = queue.pop(0)

	try:
		scrape(queue, seen_links, curr_link, sqlite_manager)
		crawl_counter += 1
	except Exception:
		print("Unable to open or parse link: {}".format( curr_link ))
