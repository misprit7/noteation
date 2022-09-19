from flask import Flask
import os

import flask
from backend.src.classes.Database import Database

app = Flask(__name__)

db = Database(username=os.environ.get("DATABASE_USERNAME"), 
              host=os.environ.get("HOST"), 
              password=os.environ.get("DATABASE_PASSWORD"), 
              cluster_name=os.environ.get("CLUSTER_NAME"))


@app.route('/events/<int:timestamp>')
def get_events(timestamp: int):
    query = f"SELECT * FROM events WHERE CAST(events.timestamp AS int) > {timestamp} ORDER BY CAST(events.timestamp AS int) ASC"
    db.connect()
    events = {"events": db.execute(statement=query)}
    db.disconnect()
    resp = flask.make_response(events) 
   
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp
    

