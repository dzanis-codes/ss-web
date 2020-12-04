
import sqlite3
conn = sqlite3.connect('result01rimi.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE results
           (name_id INTEGER PRIMARY KEY, produkta_id, prod_nosaukums, prod_links, prod_nosaukums2, prod_internal_data, cena, pilna_cena, discount, cena_pirms_atl, avots, timestamp)''')


# Save (commit) the changes
conn.commit()
conn.close()


