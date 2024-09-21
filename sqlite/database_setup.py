import sqlite3
con = sqlite3.connect("test.db")

cur = con.cursor()
#cur.execute("CREATE TABLE movie(title, year, score)")

res = cur.execute("SELECT name FROM sqlite_master")

print(res.fetchone())

# setup poetry