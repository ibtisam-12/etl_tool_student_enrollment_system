import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-1K5E5IP;"
    "DATABASE=master;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()
cursor.execute("SELECT @@VERSION;")
print(cursor.fetchone()[0])

conn.close()
print("SQL connection OK")
