

import sqlite3
conn = sqlite3.connect('result4.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE results
           (name_id INTEGER PRIMARY KEY, id, text, stavs, location, platiba, type, cena, stamp)''')

# Insert a row of data from other example
#c.execute("INSERT INTO ticker VALUES (null, '2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()
conn.close()
