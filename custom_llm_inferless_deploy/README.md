# Custom LLM Tender Extraction - Inferless Deployment

This repository contains the files needed to deploy a lightweight LLM-based tender document extraction API on [Inferless](https://inferless.com/).

## Folder Structure

```
custom_llm_inferless_deploy/
├── handler.py         # Main inference handler for Inferless
├── requirements.txt   # Python dependencies
├── README.md          # This file
```

## How to Deploy on Inferless

1. **Clone or download this folder.**

2. **Edit `handler.py` if you want to change the model or extraction schema.**

3. **Deploy on Inferless:**
   - Go to [Inferless](https://inferless.com/).
   - Create a new model deployment.
   - Upload `handler.py` and `requirements.txt`.
   - Inferless will build and deploy your model, exposing a REST API endpoint.

4. **API Usage Example:**

```python
import requests

INFERLESS_API_URL = "https://api.inferless.com/v1/your-endpoint"  # Replace with your endpoint

def inferless_llm(text):
    payload = {"text": text}
    response = requests.post(INFERLESS_API_URL, json=payload)
    return response.json()["output"]

# Example usage:
result = inferless_llm("Your tender document text here")
print(result)
```

5. **Integrate with Streamlit or other apps** by calling the Inferless API as shown above.

---

## Notes

- You can use any HuggingFace-compatible model (e.g., DistilGPT-2, TinyLlama, or your own fine-tuned model).
- For large documents, consider chunking the text and making multiple API calls.
- For custom environments, add a Dockerfile as needed.

---

**This structure is compatible with Inferless dynamic batching and scalable GPU inference.**
