from flask import Flask
# from flask_ngrok import run_with_ngrok
import os
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
    ret = db.execute(statement=query)
    print(ret)
    db.disconnect()
    return {"events": ret}
