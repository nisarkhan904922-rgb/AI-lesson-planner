# 📚 40-Minute Lesson Planner

A Streamlit app that turns a **class**, **subject** and **topic** into a complete 40-minute lesson plan with objectives, a timed activity breakdown, questions with model answers, homework and differentiation tips.

Powered by the [Groq API](https://console.groq.com) using the `openai/gpt-oss-20b` model.

## Features
- Simple form: class, subject, topic (plus optional level and notes)
- Timeline that always adds up to 40 minutes
- Recall, understanding and higher-order questions
- Homework and differentiation tips
- Download the plan as a Markdown file

## Run locally
1. Install Python 3.9+.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Get a free API key from https://console.groq.com/keys
4. Set the key:
   - **Option A (environment variable)**
     ```bash
     export GROQ_API_KEY="your_key_here"      # Windows PowerShell: $env:GROQ_API_KEY="your_key_here"
     ```
   - **Option B (Streamlit secrets)** - create `.streamlit/secrets.toml`:
     ```toml
     GROQ_API_KEY = "your_key_here"
     ```
5. Start the app:
   ```bash
   streamlit run app.py
   ```

## Deploy on Streamlit Community Cloud
1. Push `app.py`, `requirements.txt` and `README.md` to a GitHub repository.
2. Go to https://share.streamlit.io and click **Create app**.
3. Select the repo, branch (`main`) and main file `app.py`.
4. Open **Advanced settings → Secrets** and paste:
   ```toml
   GROQ_API_KEY = "your_key_here"
   ```
5. Click **Deploy**.

## Security note
Never commit your API key or `.streamlit/secrets.toml` to GitHub.

## Customizing
- Change the model by editing `MODEL` in `app.py`.
- Change the lesson structure by editing `build_prompt()` in `app.py`.
