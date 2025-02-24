import psycopg2
from db_values import DB_CONNECTION_PARAMS

CREATE_GAMES_TABLE = """
  CREATE TABLE IF NOT EXISTS games (
    id SERIAL PRIMARY KEY,
    board TEXT NOT NULL DEFAULT '---------',
    current_turn CHAR(1) NOT NULL DEFAULT 'X',
    status TEXT NOT NULL DEFAULT 'ongoing'
  );
"""

DB_MIGRATION_LIST = [
  CREATE_GAMES_TABLE
]

def run_migrations():
  try:
    conn = psycopg2.connect(**DB_CONNECTION_PARAMS)
    cur = conn.cursor()
    
    for migration in DB_MIGRATION_LIST:
      cur.execute(migration)
    
    conn.commit()
    cur.close()
    conn.close()
    
    print("Database migrations applied successfully.")
  
  except Exception as e:
    print(f"Error running migrations: {e}")

if __name__ == "__main__":
  run_migrations()
