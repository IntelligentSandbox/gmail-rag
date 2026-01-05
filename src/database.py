import os
import psycopg
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


class Database:
    def __init__(self):
        load_dotenv()
        self.db_url = os.getenv(
            "DATABASE_URL", "postgresql://user:password@localhost/emaildb"
        )
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self._connect()

    def _connect(self):
        """connect to database"""
        try:
            self.conn = psycopg.connect(self.db_url, autocommit=True)
        except Exception as e:
            raise RuntimeError(f"database connection failed: {e}")

    def _get_sql(self, filename):
        """helper to load sql from file"""
        path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "schemas", filename
        )
        with open(path) as f:
            return f.read()

    def close(self):
        """close database"""
        if self.conn:
            self.conn.close()
