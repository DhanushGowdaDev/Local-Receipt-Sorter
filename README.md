# Local Receipt Sorter

Drop in receipts and invoices; get a reviewed CSV/Excel. Runs fully offline.

## Setup
1. Install Ollama (https://ollama.com), then: `ollama pull gemma3:4b`
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

Use a bigger model with `RECEIPT_MODEL=gemma3:12b streamlit run app.py`.

## Measure accuracy
Put 30-50 receipts and a `labels.json` in `eval_set/`, then `python eval.py eval_set`.
