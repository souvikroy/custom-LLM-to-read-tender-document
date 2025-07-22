"""
Open Source Tender Document Analyzer using Gemini (Google Generative AI)
-----------------------------------------------------------------------
- Accepts multiple PDF files as input.
- Extracts information based on user-defined criteria using Gemini LLM (gemini-2.0-flash).
- Outputs structured JSON with extracted information.

Requirements:
- Python 3.8+
- google-generativeai (pip install google-generativeai)
- PyPDF2 (pip install PyPDF2)
- Set environment variable GEMINI_API_KEY with your Gemini API key.
"""

import os
import sys
import json
from typing import List, Dict
import PyPDF2
import google.generativeai as genai

# Criteria for extraction
CRITERIA = {
    "general_criteria": {
        "technical": [
            "technical qualification",
            "technical criteria",
            "technical requirement",
            "work experience",
            "project experience",
            "completion certificate",
            "work order",
            "technical capacity",
            "technical capability",
            "eligible works",
            "qualification requirement",
            "technical eligibility"
        ],
        "financial": [
            "turnover",
            "financial qualification",
            "financial criteria",
            "financial requirement",
            "annual turnover",
            "average annual turnover",
            "financial capacity",
            "financial capability",
            "net worth",
            "liquid asset",
            "solvency",
            "working capital",
            "financial statement",
            "balance sheet",
            "profit and loss",
            "financial position",
            "financial standing",
            "financial strength",
            "revenue"
        ],
        "joint_venture": [
            "joint venture",
            "jv ",
            "consortium",
            "jv criteria",
            "jv requirement",
            "lead member",
            "lead partner",
            "jv agreement",
            "jv formation"
        ],
        "commercial_clauses": [
            "earnest money",
            "emd",
            "bid security",
            "performance security",
            "security deposit",
            "retention money",
            "defect liability",
            "completion period"
        ],
        "similar_work": [
            "similar work",
            "similar nature work",
            "similar completed work",
            "similar type of work",
            "similar project"
        ]
    },
    "specific_criteria": {
        "turnover": [
            "turnover",
            "annual turnover",
            "average annual turnover",
            "financial turnover",
            "revenue"
        ],
        "emd_submission": [
            "earnest money deposit",
            "emd",
            "bid security",
            "mode of emd",
            "emd submission"
        ],
        "completion_period": [
            "completion period",
            "contract period",
            "time of completion",
            "project timeline"
        ],
        "performance_security": [
            "performance security",
            "performance guarantee",
            "performance bond"
        ],
        "security_deposit": [
            "security deposit",
            "retention money",
            "retention amount",
            "withheld amount"
        ],
        "defect_liability": [
            "defect liability",
            "defect liability period",
            "maintenance period",
            "warranty period"
        ],
        "mobilization_advance": [
            "mobilization advance",
            "mobilisation advance",
            "advance payment"
        ],
        "solvency_working_capital": [
            "solvency",
            "working capital",
            "bank solvency",
            "credit facility"
        ],
        "liquid_asset": [
            "liquid asset",
            "cash flow",
            "liquidity",
            "liquid fund"
        ],
        "price_variation": [
            "price variation",
            "price adjustment",
            "escalation clause",
            "price escalation"
        ],
        "incentive_bonus": [
            "incentive",
            "bonus clause",
            "early completion bonus",
            "performance bonus"
        ]
    }
}

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts all text from a PDF file."""
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def chunk_text(text: str, max_tokens: int = 2000) -> List[str]:
    """Splits text into chunks suitable for LLM input."""
    # Simple split by paragraphs, can be improved
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) < max_tokens * 4:  # rough char/token estimate
            current += para + "\n\n"
        else:
            chunks.append(current)
            current = para + "\n\n"
    if current:
        chunks.append(current)
    return chunks

def build_prompt(chunk: str, criteria: Dict) -> str:
    """Builds a prompt for the LLM to extract information based on criteria."""
    return f"""
You are an expert tender document analyst. Given the following text chunk from a tender document, extract all information relevant to the following criteria, grouping your findings under each heading. If nothing is found for a heading, write "Not found".

Criteria (JSON structure):
{json.dumps(criteria, indent=2)}

Text chunk:
\"\"\"
{chunk}
\"\"\"

Respond in JSON format matching the criteria structure.
"""

def analyze_pdf_with_llm(pdf_path: str, criteria: Dict) -> Dict:
    """Extracts information from a PDF using Gemini LLM."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    results = []
    for chunk in chunks:
        prompt = build_prompt(chunk, criteria)
        try:
            response = model.generate_content(prompt)
            content = response.text
            data = json.loads(content)
        except Exception as e:
            data = {"error": f"Failed to parse LLM response: {e}", "raw": content if 'content' in locals() else ""}
        results.append(data)
    # Merge results (simple merge: last non-"Not found" wins)
    merged = {}
    def merge_dicts(a, b):
        for k, v in b.items():
            if isinstance(v, dict):
                a[k] = merge_dicts(a.get(k, {}), v)
            else:
                if v != "Not found":
                    a[k] = v
        return a
    for r in results:
        merged = merge_dicts(merged, r)
    return merged

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <pdf1> <pdf2> ...")
        sys.exit(1)
    pdf_files = sys.argv[1:]
    all_results = {}
    for pdf in pdf_files:
        print(f"Analyzing {pdf} ...")
        result = analyze_pdf_with_llm(pdf, CRITERIA)
        all_results[os.path.basename(pdf)] = result
    print(json.dumps(all_results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
