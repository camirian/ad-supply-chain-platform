import sqlite3

conn = sqlite3.connect('data/supply_chain.db')
cursor = conn.cursor()

query = 'SQLQuery: SELECT "name", "location" FROM "Suppliers" WHERE "location" = \'Seattle\' LIMIT 5'
try:
    cursor.execute(query)
    print("Success")
except Exception as e:
    print(f"Error executing raw string: {e}")

query2 = 'SELECT "name", "location" FROM "Suppliers" WHERE "location" = \'Seattle\' LIMIT 5'
try:
    cursor.execute(query2)
    print(f"Success with valid string: {cursor.fetchall()}")
except Exception as e:
    print(f"Error executing valid string: {e}")
