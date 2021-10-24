import sqlite3
from flask import g


def get_db():
    g.db = sqlite3.connect('basedatos.db')
    return g.db
   

def close_db():
    if g.db is not None:
        g.db.close()



