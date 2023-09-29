import psycopg2 as db
import csv

class Config:
    def __init__(self):
        self.config = {
            "DBProject": {
                "user": "postgres",
                "password": "1234",
                "host": "127.0.0.1",
                "port": "5432",
                "database": "DBProject"
            }
        }

class Connection(Config):
    def __init__(self):
        Config.__init__(self)
        self.conn = db.connect(**self.config["DBProject"])
        self.cur = self.conn.cursor()


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self.conn

    @property
    def cursor(self):
        return self.cur

    def commit(self):
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        
    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

class Cliente(Connection):
    def __init__(self):
        Connection.__init__(self)

    def insert(self, *args):
        sql = "INSERT INTO cliente (nome, cpf, sexo, email) VALUES (%s, %s, %s, %s);"
        self.execute(sql, args)
        self.commit()

    def insert_csv(self, filename):
        try:
            data = csv.DictReader(open(filename, encoding="utf-8"))
            for row in data:
                self.insert(row["nome, cpf, sexo, email"])
            print("Registro inserido")
        except Exception as e:
            print("Erro ao inserir")

if __name__ == "__main__":
    client = Cliente()
    client.insert('as','123.456.789-12', 'M', 'test@gmail.com')
