import os
import sys
import time
import statistics

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from vd import VectorDB
from rag import RAG
from data.samples import emails, questions

ITERATIONS = 20
LIMIT = 5

vector_db = VectorDB()
vector_db.setup()
vector_db.create_embeddings(emails)
vector_db.close()

rag = RAG()

all_retrieval_times = []
all_llm_times = []
all_lengths = []
all_scores = []

for _ in range(ITERATIONS):
    for question in questions:
        start_retrieval = time.time()
        results = rag.query.search(question, limit=LIMIT)
        retrieval_time = (time.time() - start_retrieval) * 1000
        
        if results:
            start_llm = time.time()
            context = rag._format(results)
            prompt = f"""
Based on these emails, answer the question: {question}

Emails:
{context}

Answer:
"""
            response = rag.llm.respond(prompt)
            llm_time = time.time() - start_llm
            
            all_retrieval_times.append(retrieval_time)
            all_llm_times.append(llm_time * 1000)
            all_lengths.append(len(response))
            all_scores.append(max([r["similarity"] for r in results]))

rag.close()

avg_retrieval = statistics.mean(all_retrieval_times)
avg_llm = statistics.mean(all_llm_times)
avg_length = statistics.mean(all_lengths)
max_score = max(all_scores)
print(f"Tests run: {len(all_retrieval_times)}")
print(f"Retrieval: {avg_retrieval:.2f} ms")
print(f"LLM Generation: {avg_llm/1000:.2f} seconds")
print(f"Answer Length: {avg_length:.0f} characters")
print(f"Top Similarity: {max_score:.3f}")
