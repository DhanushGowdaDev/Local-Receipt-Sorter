 # 🧾 Local Receipt Sorter

**Turn receipts and invoices into structured, reviewable spreadsheets — completely offline.**

Local Receipt Sorter is a privacy-focused tool that uses local AI to extract information from receipts and invoices and organize it into CSV or Excel files. Built for offline use, it helps simplify expense tracking while keeping sensitive financial documents on your own machine.

> 🚀 **Built for the Hacktoberfest Week 2 Dev Challenge**

## ✨ Features

- 📄 **Receipt & Invoice Processing** — Extract structured information from uploaded documents.
- 🤖 **Local AI Powered** — Uses Ollama and Gemma models for on-device processing.
- 🔒 **Privacy First** — Designed to process documents locally without relying on cloud AI APIs.
- 📊 **CSV & Excel Export** — Convert extracted data into convenient spreadsheet formats.
- ✅ **Human Review** — Review extracted information before using the results.
- ⚙️ **Flexible Models** — Choose between different Gemma models based on your hardware.
- 🎯 **Accuracy Evaluation** — Evaluate extraction performance against manually labeled receipts.

## 🛠️ Tech Stack

- **Python** — Application logic and data processing
- **Streamlit** — Interactive user interface
- **Ollama** — Local AI model runtime
- **Google Gemma** — Receipt and invoice information extraction
- **CSV / Excel** — Structured data export

## 🚀 Getting Started

### Prerequisites

- Python installed on your system
- [Ollama](https://ollama.com) installed and running
- Sufficient RAM and available storage for your selected AI model

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace `YOUR_USERNAME` and `YOUR_REPOSITORY` with your GitHub details.

### 2. Download the AI model

Pull the default Gemma model using Ollama:

```bash
ollama pull gemma3:4b
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the application.

## 🧠 Choosing an AI Model

The default model is `gemma3:4b`, designed to offer a balance between capability and resource requirements.

For potentially better extraction quality, try the larger `gemma3:12b` model if your hardware can support it:

```bash
# Windows PowerShell
$env:RECEIPT_MODEL="gemma3:12b"
streamlit run app.py
```

The larger model may require significantly more memory and processing time.

## 📏 Measuring Accuracy

You can evaluate extraction performance using a collection of sample receipts and manually verified labels.

1. Create an `eval_set/` directory.
2. Add 30–50 sample receipts.
3. Add a `labels.json` file containing the expected extracted values in the format required by the evaluation script.
4. Run the evaluation:

```bash
python eval.py eval_set
```

Use the results to identify extraction errors and improve the system.

**Tip:** Use diverse receipts with different layouts, vendors, date formats, tax fields, and currencies for a more representative evaluation.

## 🔐 Privacy & Security

Privacy is a core design goal.

- AI inference is intended to run locally through Ollama.
- Receipt data can remain on your own machine.
- No cloud AI API is required for the local inference workflow.

Actual privacy depends on the application's implementation and configuration. Verify that document handling, exports, and dependencies do not transmit data externally before processing sensitive documents.

## 🗺️ Roadmap

Potential future improvements include:

- [ ] Support for more receipt and invoice formats
- [ ] Improved handling of OCR and low-quality scans
- [ ] More detailed extraction accuracy reports
- [ ] Duplicate receipt detection
- [ ] Expense categorization and monthly summaries
- [ ] Batch processing and improved spreadsheet customization

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request with a clear description.

## 🏆 Challenge

This project is being developed for the **Hacktoberfest Week 2 Dev Challenge**, exploring practical applications of local AI, document processing, and privacy-first development.

**Built with Python, Streamlit, Ollama, and Gemma.**  
*Local AI. Private documents. Structured data.*
