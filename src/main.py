import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from gmail import Gmail
from vd import VectorDB
from rag import RAG


def main():
    print("Initializing Email RAG System...")

    vector_db = VectorDB()
    vector_db.setup()

    gmail = Gmail()
    gmail.test()
    print("Fetching emails...")
    emails = gmail.fetch(max_results=20)
    print(f"Fetched {len(emails)} emails")

    vector_db.create_embeddings(emails)
    vector_db.close()

    rag = RAG()
    print("Ready!")

    while True:
        try:
            question = input("> ")
            if question.lower() in ["quit", "exit", "q"]:
                break

            if question.strip():
                print("Thinking...", end="", flush=True)
                answer = rag.ask(question)
                print("\r" + " " * 10 + "\r", end="")
                print("-" * 50)
                print(answer)
                print("-" * 50)

        except KeyboardInterrupt:
            break

    rag.close()


if __name__ == "__main__":
    main()
