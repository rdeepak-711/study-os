from fastapi import FastAPI

import mysql.connector

app = FastAPI()
# connect to mysql
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234567890"
)

# creating a cursor object
mycursor = mydb.cursor()
# create a database
mycursor.execute("CREATE DATABASE IF NOT EXISTS gate_slice")
# create a table
mycursor.execute("USE gate_slice")
mycursor.execute("CREATE TABLE IF NOT EXISTS entries(id INT AUTO_INCREMENT PRIMARY KEY, text VARCHAR(255), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

@app.post("/entries")
async def create_entry(text: str):
    sql = "INSERT INTO entries (text) VALUES (%s)"
    val = [text]
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Entry created successfully"}

@app.get("/entries")
async def get_entries():
    sql = "SELECT * FROM entries ORDER BY created_at DESC"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for x in result:
        print(x)
    return result
