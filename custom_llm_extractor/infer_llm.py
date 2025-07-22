import sys
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Example criteria (replace with your full schema as needed)
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python infer_llm.py <text_file>")
        sys.exit(1)
    text_file = sys.argv[1]
    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Use a lightweight model (change model_name as needed)
    model_name = "distilgpt2"  # Or "TinyLlama/TinyLlama-1.1B-Chat-v1.0", etc.
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    nlp = pipeline("text-generation", model=model, tokenizer=tokenizer)

    prompt = build_prompt(text, CRITERIA)
    response = nlp(prompt, max_new_tokens=1024)[0]['generated_text']
    print(response)

if __name__ == "__main__":
    main()
