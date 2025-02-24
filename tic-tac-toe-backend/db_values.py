import os
from dotenv import load_dotenv
load_dotenv()

DB_CONNECTION_PARAMS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

# Didn't end up using this, but I would make this an ENUM and refactor the code if I had time
GAME_STATUSES = {"ongoing", "X_wins", "O_wins", "draw"}
