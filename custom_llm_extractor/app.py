import streamlit as st
import PyPDF2
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Criteria schema (same as in infer_llm.py)
CRITERIA = {
    "general_criteria": {
        "technical": [
            "technical qualification",
            "technical criteria",
            "technical requirement",
            "similar work",
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

def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def build_prompt(text, criteria):
    return f"""
You are an expert tender document analyst. Given the following text chunk from a tender document, extract all information relevant to the following criteria, grouping your findings under each heading. If nothing is found for a heading, write "Not found".

Criteria (JSON structure):
{json.dumps(criteria, indent=2)}

Text chunk:
\"\"\"
{text}
\"\"\"

Respond in JSON format matching the criteria structure.
"""

def flatten_dict(d, parent_key='', sep=' > '):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep))
        else:
            items.append((new_key, v))
    return items

st.title("Custom LLM Tender Document Extractor (Lightweight Model)")

uploaded_file = st.file_uploader("Upload a Tender PDF", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting text from PDF..."):
        text = extract_text_from_pdf(uploaded_file)
    st.success("Text extracted from PDF.")
    st.text_area("Extracted Text", text, height=200)

    if st.button("Run LLM Extraction"):
        with st.spinner("Loading lightweight LLM and extracting..."):
            model_name = "distilgpt2"  # Change to "TinyLlama/TinyLlama-1.1B-Chat-v1.0" if available
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(model_name)
            nlp = pipeline("text-generation", model=model, tokenizer=tokenizer)

            prompt = build_prompt(text, CRITERIA)
            response = nlp(prompt, max_new_tokens=1024)[0]['generated_text']

            # Try to parse JSON from response
            try:
                json_start = response.find("{")
                json_data = json.loads(response[json_start:])
                st.subheader("Extracted Information (JSON)")
                st.json(json_data)
                flat = flatten_dict(json_data)
                st.subheader("Tabular View")
                st.table(flat)
            except Exception as e:
                st.error(f"Could not parse JSON from LLM output. Raw output below:\n\n{response}")
