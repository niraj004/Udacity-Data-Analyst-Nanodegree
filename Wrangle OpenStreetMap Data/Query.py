
# coding: utf-8



import sqlite3
import csv
from pprint import pprint

sqlite_file = "C:/Users/SHC User/Desktop/udacity/openstreet/map.db"
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
import pprint
cur.execute ("SELECT nodes_tags.value, COUNT(*) as num FROM nodes_tags JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='fast_food') i ON nodes_tags.id=i.id WHERE nodes_tags.key='name' GROUP BY nodes_tags.value ORDER BY num DESC LIMIT 5;")
pprint.pprint(cur.fetchall())


cur.execute("SELECT COUNT(*) FROM nodes;")
print(cur.fetchall())





cur.execute("SELECT COUNT(*) FROM ways;")
print(cur.fetchall())





cur.execute("SELECT COUNT(DISTINCT(a.uid)) FROM (SELECT DISTINCT(uid) FROM ways UNION ALL SELECT DISTINCT(uid) FROM nodes) as a;")
print(cur.fetchall())





import pprint
cur.execute("SELECT e.user, COUNT(*) as num FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e GROUP BY e.user ORDER BY num DESC LIMIT 10;")
pprint.pprint(cur.fetchall())





cur.execute("SELECT COUNT(*) FROM nodes_tags WHERE value LIKE '%Restaurant%';")
print(cur.fetchall())




cur.execute("SELECT COUNT(*) FROM nodes_tags WHERE value LIKE '%Starbucks%';")
print(cur.fetchall())









