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

