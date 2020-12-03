

import sqlite3
conn = sqlite3.connect('result02.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE results
           (name_id INTEGER PRIMARY KEY, ad_id, ad_text, stavs, location, premise_m2, land_m2, house_type, cena, ad_link, ad_source, estate_type, transaction_type, timestamp)''')


# Save (commit) the changes
conn.commit()
conn.close()
