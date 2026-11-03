import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Se estiver a usar o pooler (recomendado):
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres.smohwgxtukmsuayyuxqu:Corridaderua@aws-0-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require")
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn



