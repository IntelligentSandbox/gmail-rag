import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from vd import VectorDB
from rag import RAG
from data.samples import emails, questions


def main():
    vector_db = VectorDB()
    vector_db.setup()
    vector_db.create_embeddings(emails)
    vector_db.close()
    
    rag = RAG()
    
    for question in questions:
        print(f"Q: {question}")
        answer = rag.ask(question)
        print(f"A: {answer}")
        print("-" * 60)
    
    rag.close()


if __name__ == "__main__":
    main()