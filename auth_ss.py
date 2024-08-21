import singlestoredb as s2
from dotenv import load_dotenv
import os


def singlestore_auth():

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
    return conn


# conn = auth_ss()
# with conn.cursor() as cur:
#     sql = cur.execute("SELECT * FROM embeddings")
#     print(sql)
