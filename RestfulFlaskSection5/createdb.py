import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

cursor.execute("create table if not exists users (id INTEGER PRIMARY KEY,name text,password text)")

users = [(1, "Anand", "Anand"), (2, "Ramya", "Ramya")]

cursor.executemany("insert into users values (?,?,?)", users)

rows = list(cursor.execute("select * from users"))

print(rows)

connection.commit()

connection.close()

connection = sqlite3.connect("data.db")
cursor = connection.cursor()
cursor.execute("Create table if not exists items(item_name primary key,price real)")
connection.commit()
connection.close()