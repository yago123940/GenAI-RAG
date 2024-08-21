import singlestoredb as s2
from dotenv import load_dotenv
import os

load_dotenv("config.env")

user_ss = os.getenv("SINGLESTORE_USER")
password_ss = os.getenv("SINGLESTORE_PASSWORD")


# Create a connection to the database
conn = s2.connect(
    user_ss
    + ":"
    + password_ss
    + "@svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com:3333/db_yago_3770b"
)
# Check if the connection is open
with conn:
    with conn.cursor() as cur:
        flag = cur.is_connected()
        print(flag)


with conn.cursor() as cur:
    cur.execute("SELECT * FROM embeddings")
    for row in cur.fetchall():
        print(row)
