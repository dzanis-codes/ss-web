
import csv
import sqlite3

db_file = "C:\sqlite\db\pythonsqlite.db"


conn = sqlite3.connect(db_file)
cur = conn.cursor()
cur.execute("SELECT * FROM results")

rows = cur.fetchall()

for row in rows:
    for entry in row:
        print(row)
        print(entry)




##delimiterus labāk noteikt ;;
csv.register_dialect('unixpwd', delimiter=';;', quoting=csv.QUOTE_NONE)
f = open('test2.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(f, 'unixpwd')
writer.writerow(('ßßßüuhěelloworld',
                 'hello bye'))
f.close()
