import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:[SUA-SENHA]@db.smohwgxtukmsuayyuxqu.supabase.co:5432/postgres")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn
