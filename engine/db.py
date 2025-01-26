import csv
import sqlite3

con = sqlite3.connect("star.db")
cursor = con.cursor()


# Create table for applications
# query = "CREATE TABLE IF NOT EXISTS applications(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)
#
# # Insert example data into applications table
# query = "INSERT INTO applications VALUES (null,'one note', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE')"
# cursor.execute(query)
# con.commit()
#
# query = "INSERT INTO applications VALUES (null,'vs code', 'D:\\Microsoft VS Code\\Code.exe')"
# cursor.execute(query)
# con.commit()

# Create table for app_command
# Create table for app_command
query = "CREATE TABLE IF NOT EXISTS app_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)
con.commit()

app_name = "vs code"
cursor.execute('SELECT path FROM app_command WHERE name = ?', (app_name,))
results = cursor.fetchall()

