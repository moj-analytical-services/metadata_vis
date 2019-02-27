import sqlite3
conn = sqlite3.connect("app.db")

sql = "SELECT * FROM fulltextsearch WHERE fulltextsearch MATCH 'sensor' ORDER BY rank;"

result = conn.execute(sql)

all = result.fetchall()

print(all)