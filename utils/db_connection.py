import os
import psycopg2
import logging
# from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv

logger = logging.getLogger("airflow.task")

_ = load_dotenv()

def make_db_connection() -> psycopg2.extensions.connection:
    """Create a Postgres DB connection"""
    try:
        conn = psycopg2.connect(
            database=os.getenv('POSTGRES_DB'),
            host=os.getenv('POSTGRES_HOST'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            port=os.getenv('POSTGRES_PORT')
        )
        conn.autocommit = False
        logger.info(f"database:{os.getenv('POSTGRES_DB')}, host:{os.getenv('POSTGRES_HOST')}, user:{os.getenv('POSTGRES_USER')}, password:{os.getenv('POSTGRES_PASSWORD')}, port:{os.getenv('POSTGRES_PORT')}")
        # conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    except psycopg2.OperationalError as e:
        raise Exception(f'Could not create Postgres connection: {e}')
    
    return conn

# def make_connection2():
#     engine = create_engine(f'postgresql+psycopg2://{os.getenv("USER")}:{os.getenv("PASSWORD")}@{os.getenv("HOST")}/{os.getenv("DATABASE")}')
#     print(engine)

if __name__ == '__main__':
    conn = make_db_connection()
    cur = conn.cursor()
    # cur.execute("select 1")
    # print(cur.fetchall())