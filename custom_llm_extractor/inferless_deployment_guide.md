# Deploying Your Custom LLM Extraction Pipeline on Inferless GPU

## 1. Prepare Your Inference Handler

Inferless expects a handler.py file with a `infer` function. Example for DistilGPT-2:

```python
# handler.py
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import json

# Load model and tokenizer at startup
model_name = "distilgpt2"  # Or your fine-tuned model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
nlp = pipeline("text-generation", model=model, tokenizer=tokenizer)

def build_prompt(text, criteria):
    return f'''
You are an expert tender document analyst. Given the following text chunk from a tender document, extract all information relevant to the following criteria, grouping your findings under each heading. If nothing is found for a heading, write "Not found".

Criteria (JSON structure):
{json.dumps(criteria, indent=2)}

Text chunk:
\"\"\"
{text}
\"\"\"

Respond in JSON format matching the criteria structure.
'''

# Example criteria (replace with your full schema)
CRITERIA = { ... }  # Paste your criteria dict here

def infer(request):
    # request is a dict with a "text" field
    text = request.get("text", "")
    prompt = build_prompt(text, CRITERIA)
    response = nlp(prompt, max_new_tokens=1024)[0]['generated_text']
    return {"output": response}
```

## 2. Package and Upload

- Place handler.py and any requirements.txt in a directory.
- In requirements.txt, include:
  ```
  transformers
  torch
  ```
- Zip the directory if required.

## 3. Deploy on Inferless

- Go to https://inferless.com/ and sign up/log in.
- Create a new model deployment.
- Upload your handler.py and requirements.txt, or point to your HuggingFace model.
- Inferless will build and deploy your model, exposing a REST API endpoint.

## 4. Update Your Streamlit App

Replace the local LLM inference with a call to the Inferless API:

```python
import requests

INFERLESS_API_URL = "https://api.inferless.com/v1/your-endpoint"  # Replace with your endpoint

def inferless_llm(text):
    payload = {"text": text}
    response = requests.post(INFERLESS_API_URL, json=payload)
    return response.json()["output"]

# In your Streamlit app, replace the LLM call:
if st.button("Run LLM Extraction"):
    with st.spinner("Calling Inferless LLM API..."):
        response = inferless_llm(text)
        # Try to parse JSON from response as before
```

## 5. Notes

- You can upload a quantized or fine-tuned model to Inferless for better performance and lower cost.
- Inferless handles GPU scaling and API management for you.
- For large PDFs, consider chunking the text and making multiple API calls.

---

**This guide provides the steps to deploy your LLM extraction pipeline on Inferless GPU and connect it to your Streamlit or other client apps.**
