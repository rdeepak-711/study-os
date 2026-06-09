from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import os
import mysql.connector

app = FastAPI()
# connect to mysql
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.environ.get("MYSQL_PASSWORD")
)

class DBEntry(BaseModel):
    text: str

# creating a cursor object
mycursor = mydb.cursor()
# create a database
mycursor.execute("CREATE DATABASE IF NOT EXISTS gate_slice")
# create a table
mycursor.execute("USE gate_slice")
mycursor.execute("CREATE TABLE IF NOT EXISTS entries(id INT AUTO_INCREMENT PRIMARY KEY, text VARCHAR(255), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

@app.post("/entries")
async def create_entry(entry: DBEntry):
    sql = "INSERT INTO entries (text) VALUES (%s)"
    val = [entry.text]
    mycursor.execute(sql, val)
    id_no = mycursor.lastrowid
    mydb.commit()
    return {"message": "Entry created successfully", "id":id_no}

@app.get("/entries")
async def get_entries():
    sql = "SELECT * FROM entries ORDER BY id DESC"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result

@app.get("/entries/{id}")
async def get_specific_entry(id):
    sql = "SELECT * FROM entries where id=(%s)"
    val = [id]
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result

@app.put("/entries/{id}")
async def add_specific_entry(id, entry: DBEntry):
    sql = "UPDATE entries SET text=(%s) where id=(%s)"
    val = [entry.text, id]
    mycursor.execute(sql, val)
    rowCount = mycursor.rowcount
    if rowCount==0:
        raise HTTPException(status_code=404, detail="Item not found")
    mydb.commit()
    return {"message": "Entry updated successfully", "id":id}

@app.delete("/entries/{id}")
async def delete_specific_entry(id):
    sql = "DELETE FROM entries where id=(%s)"
    val = [id]
    mycursor.execute(sql, val)
    rowCount = mycursor.rowcount
    if rowCount==0:
        raise HTTPException(status_code=404, detail="Item not found")
    mydb.commit()
    return {"message": "Entry deleted successfully", "id":id}