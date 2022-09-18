import psycopg2


class Database(): 
    
    def __init__(self, username: str, host: str, password: str, cluster_name: str): 
        self.username = username
        self.host = host
        self.password = password
        self.cluster_name = cluster_name
    
    
    def connect(self): 
        self.connection = psycopg2.connect(dsn=self.host, application_name=self.cluster_name)
    
    
    def disconnect(self): 
        self.connection.close()
        
        
    def execute(self, statement: str): 
        try: 
            with self.connection.cursor() as cursor: 
                cursor.execute(statement)
                self.connection.commit()
                return cursor.fetchall()
        except psycopg2.ProgrammingError as e: 
            print(e)
            return 
    
                    