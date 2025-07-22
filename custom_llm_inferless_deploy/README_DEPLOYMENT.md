# Inferless Deployment Packaging Instructions

To avoid "app.py file is not present" errors, follow these steps:

1. Ensure your deployment folder contains these files at the top level:
   - app.py
   - requirements.txt
   - README.md

2. **Do NOT upload the folder itself.**  
   Instead, upload a ZIP file containing these files at the root.

3. To create the correct ZIP:
   - Open the custom_llm_inferless_deploy/ folder.
   - Select app.py, requirements.txt, and README.md (not the folder itself).
   - Right-click and choose "Send to > Compressed (zipped) folder" (Windows) or use your OS's zip tool.
   - The resulting ZIP should contain:
     ```
     app.py
     requirements.txt
     README.md
     ```
     (no subfolder in the ZIP)

4. Upload this ZIP to Inferless.

**If you still see the error, double-check:**
- The file is named exactly app.py (not app.py.txt, not App.py, no extra spaces).
- The ZIP does not contain a subfolder.

This will resolve the "app.py file is not present" error on Inferless.
