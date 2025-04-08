import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

user = os.getenv("DB_USER")
password = quote_plus(os.getenv("DB_PASS"))
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
name = os.getenv("DB_NAME")

DB_URI = f"postgresql://{user}:{password}@{host}:{port}/{name}"
