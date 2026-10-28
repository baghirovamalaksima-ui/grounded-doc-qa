# Grounded Document Q&A

Junior portfolio project: local Markdown retrieval, source citations, conservative abstention, and optional Ollama-assisted quote selection. Developed with AI assistance; review and understand the implementation before claiming ownership in interviews.

## Run on Windows (Python 3.11+)

```powershell
py -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python rag.py "How many paid vacation days?"
.\.venv\Scripts\python -m pytest -q
```

The default works offline with no API key or model. It retrieves paragraphs and returns the best matching paragraph verbatim with a stable file/paragraph citation. Sample data is fictional and English only.

## Optional LLM path

Install Ollama yourself, run its local service and download a model of your choice. Then run `python rag.py "How many paid vacation days?" --model YOUR_INSTALLED_MODEL`. Only retrieved paragraphs are sent to the service at `127.0.0.1:11434`. The model selects exact quotations in JSON; invalid, fabricated, or missing citations cause abstention. Connection and malformed-output failures also abstain. This is constrained LLM-assisted RAG, not free-form generation. No real model execution is claimed by the offline tests.

## Design and limits

1. Split Markdown files on blank lines; retain deterministic source IDs.
2. Rank using unique query-token overlap divided by square root of paragraph length.
3. Require two matching content words before answering.
4. Validate every returned quote against its cited retrieved paragraph.

Exact quotation checking proves attribution, not relevance, factual truth, completeness, or prompt-injection immunity. Malicious or outdated source text can still be quoted. Lexical retrieval misses synonyms, negation and multilingual queries. Paragraph IDs change if documents are edited. No embeddings, PDF parsing, vector database, access control or production hardening is claimed.

## Explain in an interview

Walk through `load_documents`, `retrieve`, `ask`, and `grounded`. Explain why unsupported queries abstain, why source overlap cannot establish truth, and how you would add labeled paraphrases and embedding retrieval. Tests cover attribution, unknown questions, deterministic ranking, invalid parameters and simulated LLM failure/fabrication.

See `VALIDATION.md` for the actually executed checks.
