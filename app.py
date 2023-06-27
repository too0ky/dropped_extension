import os
import psycopg2
import configparser
import json
from flask import Flask, request
import pandas as pd

config = configparser.ConfigParser()
config.read('database.env')

db_host = config['atlas_backend_ro']['host']
db_database_name = config['atlas_backend_ro']['database']
db_user = config['atlas_backend_ro']['user']
db_password = config['atlas_backend_ro']['password']
db_port = config['atlas_backend_ro']['port']

app = Flask(__name__)

conn = psycopg2.connect(database = db_database_name,
                        host = db_host,
                        user = db_user,
                        password = db_password,
                        port = db_port)

cursor = conn.cursor()


document_push_id = input("Enter the document_push_id: ")

SELECT_ALL_URLS = f"SELECT documents.url, documents.dropped_reason from documents where documents.document_push_id = {document_push_id} AND dropped = True;"
#LIMIT 20

@app.route("/api/documents", methods = ["GET"])
def get_all_urls():
    with conn:
        cursor.execute(SELECT_ALL_URLS)
        urls = cursor.fetchall()
        # print(urls)
        if urls:
            result=[]
            for url in urls:
                result.append({'url':url[0], 'dropped_reason': url[1]})
                json_result = json.dumps(result)
            print(json_result) 
            return json_result 
        else:
            return {'error': f'Urls not found'}, 404
    cursor.close()
    conn.close()
        
get_all_urls()

if __name__ == '__main__':
    app.run(debug=False)

