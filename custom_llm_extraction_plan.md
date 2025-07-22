# Plan: Building a Custom LLM for Tender Document Information Extraction

## Objective
Develop a custom LLM-based pipeline to extract structured information from tender documents (PDFs) according to the provided schema.

---

## 1. Data Preparation

- **Collect Tender PDFs**: Gather a diverse set of tender documents.
- **Annotation**: For each PDF, create a JSON file with extracted fields matching the schema:
  - `general_criteria` (technical, financial, joint_venture, commercial_clauses)
  - `specific_criteria` (turnover, emd_submission, etc.)
- **Dataset Example**:
  - `tender1.pdf`
  - `tender1.json` (ground truth)

---

## 2. Preprocessing

- **Extract Text**: Use PyPDF2 or pdfplumber to extract text from PDFs.
- **Align Data**: Pair extracted text with the corresponding JSON labels.

---

## 3. Model Selection

- **Choose a Lightweight Base Model**: Use an open-source, resource-efficient LLM such as:
  - TinyLlama (1.1B parameters): https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0
  - Phi-2 (2.7B parameters): https://huggingface.co/microsoft/phi-2
  - DistilGPT-2 (smallest GPT-2 variant): https://huggingface.co/distilgpt2
  - Mistral-7B (quantized, e.g., 4-bit): https://huggingface.co/mistralai/Mistral-7B-v0.1
- **Why Lightweight?**
  - Lower memory and compute requirements (can run on CPU or low-end GPU)
  - Faster inference and lower cost
- **Frameworks**: Use HuggingFace Transformers for fine-tuning and inference.
- **Tip**: For even lower resource usage, use quantized models (e.g., bitsandbytes, GGUF/llama.cpp).


## 4. Fine-Tuning

- **Format Training Data**: For each sample, create a prompt/response pair:
  - **Prompt**: "Extract the following fields from the tender document: [schema]. Document: [text]"
  - **Response**: The corresponding JSON.
- **Training**: Fine-tune the model using supervised learning (SFT).
  - Use HuggingFace Trainer or similar.
  - Recommended hardware: GPU (A100, T4, or similar).

---

## 5. Inference Pipeline

- **PDF → Text**: Extract text from new PDFs.
- **Prompt LLM**: Use the same prompt format as training.
- **Parse Output**: Convert LLM output to JSON, handle errors.

---

## 6. Integration

- **Replace Gemini API**: In your Python code, replace Gemini API calls with local LLM inference.
- **Example (using HuggingFace Transformers):**
  ```python
  from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

  model_name = "your-finetuned-model"
  tokenizer = AutoTokenizer.from_pretrained(model_name)
  model = AutoModelForCausalLM.from_pretrained(model_name)
  nlp = pipeline("text-generation", model=model, tokenizer=tokenizer)

  prompt = build_prompt(chunk, CRITERIA)
  response = nlp(prompt, max_new_tokens=2048)[0]['generated_text']
  # Parse response as JSON
  ```

---

## 7. Optional: Evaluation

- **Metrics**: Use F1, precision, recall on a held-out test set.
- **Manual Review**: Spot-check outputs for accuracy.

---

## 8. Deployment

- **Local Inference**: Run on a local server or workstation.
- **API Wrapper**: Optionally, expose as a REST API for integration.

---

## 9. Tools & Resources

- [HuggingFace Transformers](https://huggingface.co/docs/transformers/index)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [pdfplumber](https://pypi.org/project/pdfplumber/)
- [Llama 3](https://ai.meta.com/llama/)
- [Mistral](https://mistral.ai/)

---

## Notes

- Building a high-quality custom LLM requires a sufficiently large and well-annotated dataset.
- If you lack GPU resources, consider using smaller models or cloud-based training.
- For rapid prototyping, you can use existing LLMs with prompt engineering before full fine-tuning.

---

**This plan provides a practical roadmap for building and integrating a custom LLM for your tender document extraction use case.**
