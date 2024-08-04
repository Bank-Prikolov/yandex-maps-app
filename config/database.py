import os
import sqlite3


if not os.path.exists("db"):
    os.makedirs("db")

con = sqlite3.connect("db/YandexMapsApp.sqlite")
cur = con.cursor()
