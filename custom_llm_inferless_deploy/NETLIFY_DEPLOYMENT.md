# Deploying a Frontend for Your LLM Extractor on Netlify

Netlify only supports static sites (HTML, JS, CSS, React, etc.), not Python APIs. To use Netlify with your LLM backend:

## 1. Deploy Your LLM API

- Deploy your Python LLM inference API to Inferless, HuggingFace Inference Endpoints, or another backend platform.
- Obtain the public API endpoint URL.

## 2. Build a Frontend

- Create a simple frontend (React, HTML/JS, or similar) that lets users upload a PDF, extracts text (in-browser or via API), and calls your LLM API endpoint.
- Example: Use React or plain HTML/JS to POST the extracted text to your LLM API and display the results.

## 3. Deploy the Frontend to Netlify

- Place your frontend code (index.html, JS, CSS, etc.) in a folder (e.g., `frontend/`).
- Push the folder to a GitHub repo or drag-and-drop it into Netlify's dashboard.
- Netlify will host your static site.

## 4. Connect Frontend to Backend

- In your frontend code, set the API endpoint to your deployed LLM API (Inferless, etc.).
- Example (JS):
  ```js
  fetch("https://api.inferless.com/v1/your-endpoint", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: extractedText })
  })
  .then(res => res.json())
  .then(data => { /* display results */ });
  ```

## 5. (Optional) Use Netlify Functions for Simple Serverless Logic

- For simple serverless functions (Node.js), you can use Netlify Functions, but not for Python LLM inference.

---

**Summary:**  
- Deploy your Python LLM API to a backend platform (not Netlify).
- Deploy your frontend to Netlify and connect it to your API.

If you need a sample React or HTML/JS frontend for this workflow, let me know!
