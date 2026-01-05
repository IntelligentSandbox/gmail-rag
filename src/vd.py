import os
import sys
from database import Database

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


class VectorDB(Database):
    def setup(self):
        """setup pgvector extension and create table"""
        with self.conn.cursor() as cur:
            cur.execute(self._get_sql("create_table.sql"))

    def create_embeddings(self, emails):
        """convert emails to vectors and store in database"""
        texts = []
        for e in emails:
            enhanced_content = (
                f"From: {e['sender']} Subject: {e['subject']} {e['content']}"
            )
            texts.append(enhanced_content)
        embeddings = self.model.encode(texts)

        insert_sql = self._get_sql("insert_email.sql")

        with self.conn.cursor() as cur:
            for i, email in enumerate(emails):
                vec = embeddings[i]
                cur.execute(
                    insert_sql,
                    (
                        email["id"],
                        email["sender"],
                        email["recipient"],
                        email["subject"],
                        email["body"],
                        email["content"],
                        email["date"],
                        email["thread_id"],
                        vec.tolist(),
                    ),
                )

    def close(self):
        """close database"""
        if self.conn:
            self.conn.close()
