from classes.Database import Database
from handlers.AdHawk import AdHawkHandler
import os
from dotenv import load_dotenv


def main(): 
    load_dotenv('.env')
    database = Database(os.environ.get("DATABASE_USERNAME"), os.environ.get("HOST"),
                os.environ.get("DATABASE_PASSWORD"), os.environ.get("CLUSTER_NAME"))
    handler = AdHawkHandler(database)
    handler.quickstart()


if __name__ == '__main__':
    main()