import requests
import os
import json
from dotenv import load_dotenv
from auth_ss import singlestore_auth

load_dotenv("config.env")


conn = singlestore_auth()

with conn.cursor() as cur:
    sql = cur.execute("SELECT * FROM embeddings")
    print(sql)
