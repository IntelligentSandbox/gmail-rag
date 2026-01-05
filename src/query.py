import os
import sys
from database import Database

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


class Query(Database):
    def _execute(self, sql_file, params, operation_name):
        """helper function to execute SQL and format results"""
        try:
            sql = self._get_sql(sql_file)

            with self.conn.cursor() as cur:
                cur.execute(sql, params)
                results = cur.fetchall()

            return [
                {
                    "email_id": row[0],
                    "sender": row[1],
                    "recipient": row[2],
                    "subject": row[3],
                    "body": row[4],
                    "content": row[5],
                    "date": row[6],
                    "thread_id": row[7],
                    "similarity": row[8] if len(row) > 8 else None,
                }
                for row in results
            ]
        except Exception as e:
            raise RuntimeError(f"{operation_name} failed: {e}")

    def search(self, query_text, limit=5):
        """search for similar emails"""
        query_vec = self.model.encode(query_text)
        return self._execute(
            "search_email.sql",
            (query_vec.tolist(), query_vec.tolist(), limit),
            "search",
        )

    def search_by_sender(self, sender_name, limit=5):
        """search emails from specific sender"""
        return self._execute(
            "search_by_sender.sql", (f"%{sender_name}%", limit), "search by sender"
        )

    def get_thread(self, thread_id):
        """get all emails in a thread"""
        return self._execute("get_thread.sql", (str(thread_id),), "get thread")

    def search_with_threads(self, query_text, limit=5):
        """search for similar emails and include their full threads"""
        initial_results = self.search(query_text, limit)
        seen_ids = {r["email_id"] for r in initial_results}
        all_results = list(initial_results)

        for tid in {r["thread_id"] for r in initial_results if r.get("thread_id")}:
            for email in self.get_thread(tid):
                if email["email_id"] not in seen_ids:
                    seen_ids.add(email["email_id"])
                    all_results.append(email)

        return all_results
