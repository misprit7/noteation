from flask import Flask
# from flask_ngrok import run_with_ngrok
import os

import flask
from backend.src.classes.Database import Database

app = Flask(__name__)
# run_with_ngrok(app)


db = Database(username=os.environ.get("DATABASE_USERNAME"), 
              host=os.environ.get("HOST"), 
              password=os.environ.get("DATABASE_PASSWORD"), 
              cluster_name=os.environ.get("CLUSTER_NAME"))


@app.route('/events/<int:timestamp>')
def get_events(timestamp: int):
    query = f"SELECT * FROM events WHERE CAST(events.timestamp AS int) > {timestamp}"
    db.connect()
    events = {"events": db.execute(statement=query)}
    print(events)
    resp = flask.make_response(events) 
    # resp.headers = {
    #     'Access-Control-Allow-Origin': 'http://localhost:3000', 
    #     'Access-Control-Allow-Methods': 'POST, PUT, PATCH, GET, DELETE, OPTIONS',
    #     'Access-Control-Allow-Headers': 'Origin, X-Api-Key, X-Requested-With, Content-Type, Accept, Authorization'
    # }
    resp.headers["Access-Control-Allow-Origin"] = "*"

    print(resp.data)
    return resp
    

    
    print(resp)
    db.disconnect()
    return resp
