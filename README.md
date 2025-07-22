# 📝 Tender LLM – Automated Tender Information Extraction

A project to develop a custom Large Language Model (LLM) pipeline for extracting structured information from government tender documents in PDF format.

---

## 📦 Project Structure

```
tender LLM/
├── .gitignore
├── check_env.py                # Script to check installed Python environment
├── custom_llm_extraction_plan.md  # Core documentation for the extraction system
├── .git/                       # Git repository metadata
```

---

## 🎯 Objective

Build an LLM-powered document understanding system to extract structured data from tender PDFs based on a predefined schema.

---

## 📋 Extraction Schema

The pipeline extracts data under two main categories:

### 🔹 General Criteria
- Technical
- Financial
- Joint Venture
- Commercial Clauses

### 🔹 Specific Criteria
- Turnover
- EMD Submission
- Others (custom fields based on tender)

---

## 🔧 How It Works

### 1. Data Preparation
- Collect multiple tender PDF files
- Annotate each file with a corresponding `.json` file containing labeled information based on the schema.

### 2. Preprocessing
- Extract raw text from PDFs using tools like `pdfplumber` or `PyPDF2`
- Align the raw text with JSON-labeled fields for training and evaluation

### 3. Model Integration
- Use a fine-tuned transformer model or LLM API (e.g., OpenAI, Cohere) to extract schema-aligned data
- Prompt engineering and extraction plan defined in `custom_llm_extraction_plan.md`

---

## 🛠️ Environment Setup

Make sure you have Python installed. Then run:

```bash
python check_env.py
```

This prints the current Python path and all installed packages, helping ensure environment consistency.

---

## 🗂️ Data Format

```
/data/
├── tender1.pdf
├── tender1.json
├── tender2.pdf
├── tender2.json
...
```

Each `.json` should include structured fields matching the schema.

---

## 🚧 TODO

- [ ] Implement PDF text extraction
- [ ] Define JSON schema validator
- [ ] Build prompt templates for each extraction type
- [ ] Fine-tune or plug into LLM API
- [ ] Add evaluation and logging pipeline

---

## 📄 License

MIT License (add your own license here)
