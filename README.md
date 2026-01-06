# Personal Gmail RAG System

Local RAG pipeline that ingests Gmail emails, stores them in a vector database, and supports querying via an open-source LLM. Keeps previous email context for follow-up questions.

## Install

```bash
python setup.py
```

## Activate

```bash
source venv/bin/activate
```

## Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Search **API & Services**
3. Open **Credentials**
4. Click **Create Credentials** → **OAuth Client ID**
5. Select **Desktop app**
6. Download the JSON file
7. Move it to `src/credentials.json`

Enable the [Gmail API](https://console.cloud.google.com/apis/api/gmail.googleapis.com/metrics).

## Ollama Model

Install the required Mistral model:

```bash
ollama pull mistral
```

The default mistral model uses Q4_K_M quantization (4.4GB size vs 14GB FP32) for optimal performance.

## Database

```bash
./setup_database.sh
```

## Usage

```bash
python src/main.py
```

## Benchmark

```bash
python benchmark.py
```

## Demo

> [!IMPORTANT]
> Please follow previous steps to setup the enviornment!

**Run demo**

```bash
python demo.py
```

## References


- [Gmail API Quickstart](https://developers.google.com/workspace/gmail/api/quickstart/python)
- [Gmail Search Operators](https://support.google.com/mail/answer/7190)
- [Gmail API Message Format](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages)
- [Gmail API attachments Format](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages.attachments/get)
- [Email Header Specifications](https://datatracker.ietf.org/doc/html/rfc2822)
- [Refine searches in Gmail](https://support.google.com/mail/answer/7190)
- [Installing PostgreSQL + pgvector on Debian](https://dev.to/farez/installing-postgresql-pgvector-on-debian-fcf)
- [pypdf docs](https://pypdf.readthedocs.io/en/stable/)
- [Mime types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types)
- [Improving Performance of PostgreSQL queries](https://dev.to/jacobandrewsky/improving-performance-of-postgresql-queries-1h7o)
- [pytesseract project desc](https://pypi.org/project/pytesseract/)
- [Vector Similarity Search with PostgreSQL’s pgvector – A Deep Dive](https://severalnines.com/blog/vector-similarity-search-with-postgresqls-pgvector-a-deep-dive/)
- [Introduction: From Distance to Cosine Similarity](https://codesignal.com/learn/courses/advanced-querying-with-pgvector/lessons/extracting-cosine-similarity-scores-with-pgvector)
- [Unlocking the Power of Sentence Embeddings with all-MiniLM-L6-v2](https://medium.com/@rahultiwari065/unlocking-the-power-of-sentence-embeddings-with-all-minilm-l6-v2-7d6589a5f0aa)
- [Mistral-7B](https://mistral.ai/news/announcing-mistral-7b)
- [LangChain](https://www.pinecone.io/learn/series/langchain/langchain-conversational-memory/)
