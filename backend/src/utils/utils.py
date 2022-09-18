from typing import List
import time
import sys
sys.path.append('../../')
from backend.src.classes.Database import Database
from backend.src.classes.Event import Event


def log_event(db: Database, event: Event):
    db.connect() 
    statement = f"INSERT INTO public.events ({', '.join(event.get_properties())}) VALUES {tuple(event.get_values())};"
    db.execute(statement=statement)    
    db.disconnect()

def create_table(db: Database): 
    db.connect()
    statement = "CREATE TABLE IF NOT EXISTS events (timestamp VARCHAR(255) PRIMARY KEY, event_type VARCHAR(225));"
    db.execute(statement)
    db.disconnect()

    