# Tender Document Analyzer (Open Source, Mixtral LLM via Ollama)

This tool analyzes multiple tender PDF documents and extracts structured information based on customizable technical, financial, and commercial criteria using the open-source Mixtral LLM (via [Ollama](https://ollama.com/)).

## Features

- **Multi-PDF Input:** Analyze any number of tender documents at once.
- **LLM-Powered Extraction:** Uses Mixtral LLM for robust, context-aware information extraction.
- **Customizable Criteria:** Easily modify the extraction criteria in `main.py`.
- **Structured Output:** Results are output as JSON, grouped by document and criteria.
- **Open Source:** MIT licensed, easy to extend.

## Requirements

- Python 3.8+
- [Ollama](https://ollama.com/) (running locally)
- Mixtral model pulled via Ollama
- Python packages: see `requirements.txt`

## Setup

1. **Install Ollama and Pull Mixtral Model**
   - Download and install Ollama: https://ollama.com/download
   - Pull the Mixtral model:
     ```
     ollama pull mixtral
     ```

2. **Clone this repository and install Python dependencies**
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Place your tender PDF files in a directory.

2. Run the analyzer:
   ```
   python main.py path/to/tender1.pdf path/to/tender2.pdf ...
   ```

3. The output will be a JSON object printed to the console, mapping each PDF filename to its extracted information.

## Customizing Criteria

Edit the `CRITERIA` dictionary in `main.py` to change or expand the extraction targets.

## Example Output

```json
{
  "tender1.pdf": {
    "general_criteria": {
      "technical": "...",
      "financial": "...",
      ...
    },
    "specific_criteria": {
      "turnover": "...",
      ...
    }
  },
  "tender2.pdf": {
    ...
  }
}
```

## License

MIT License
