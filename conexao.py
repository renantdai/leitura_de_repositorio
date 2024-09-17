import mysql.connector
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

class BancoDeDados:
    def __init__(self):
        self.connection = mysql.connector.connect(host=config['host'], port=config['port'], user=config['user'], passwd=config['password'], database=config['database'])
        self.cursor = self.connection.cursor()

    def realizar_consulta(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()