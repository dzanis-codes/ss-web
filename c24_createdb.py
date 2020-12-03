import sqlite3
conn = sqlite3.connect('result01c24.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE results
           (name_id INTEGER PRIMARY KEY, ad_id, apraksts, stavs, adrese, premise_m2, land_m2, cena, cena_m2, ad_link, ad_source, estate_type, istabas, timestamp)''')


# Save (commit) the changes
conn.commit()
conn.close()
