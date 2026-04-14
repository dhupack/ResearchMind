# Multi-Agent Research System

A Python-based multi-agent research assistant that searches the web, reads source content, writes a structured report, and critiques the output.

The project uses LangChain agents/chains, Google Gemini, Tavily search, and a Streamlit UI.

## Features

- Multi-step research pipeline:
  - Search agent: gathers recent web results
  - Reader agent: scrapes content from a selected URL
  - Writer chain: generates a detailed report
  - Critic chain: reviews and scores the report
- Streamlit interface for interactive usage (`app.py`)
- CLI workflow for terminal-based usage (`pipeline.py`)
- Markdown report download from the UI

## Project Structure

- `app.py` - Streamlit frontend and pipeline execution UI
- `pipeline.py` - CLI pipeline runner
- `agents.py` - LangChain agent and chain definitions
- `tools.py` - custom tools (`web_search`, `scrape_url`)
- `requirements.txt` - Python dependencies
- `.env` - API keys (local only; do not commit)

## Requirements

- Python 3.10+ recommended
- Tavily API key
- Google Gemini API key

## Installation

1. Clone or open the project folder.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create/update `.env` in the project root:

```env
TAVILY_API_KEY=your_tavily_key
Gemini_API_KEY=your_gemini_key
```

Notes:

- `TAVILY_API_KEY` is required by `tools.py`.
- `agents.py` uses `ChatGoogleGenerativeAI`, which commonly expects `GOOGLE_API_KEY`.  
  If you see auth errors with `Gemini_API_KEY`, set:

```env
GOOGLE_API_KEY=your_gemini_key
```

## Run the App (Streamlit)

```bash
streamlit run app.py
```

Then open the local Streamlit URL in your browser, enter a topic, and run the pipeline.

## Run from CLI

```bash
python pipeline.py
```

You will be prompted to enter a research topic. The pipeline then runs all four steps and prints output to the terminal.

## How the Pipeline Works

1. **Search Agent** (`build_search_agent`) uses Tavily web search.
2. **Reader Agent** (`build_reader_agent`) scrapes selected source content.
3. **Writer Chain** produces a structured report:
   - Introduction
   - Key Findings
   - Conclusion
   - Sources
4. **Critic Chain** evaluates the report with:
   - Score
   - Strengths
   - Areas to Improve
   - One-line verdict

## Dependencies

Key libraries used:

- `langchain`, `langchain-core`, `langchain-community`
- `langchain-google-genai`, `google-generativeai`
- `tavily-python`
- `requests`, `beautifulsoup4`, `lxml`, `html5lib`
- `python-dotenv`
- `streamlit`

## Troubleshooting

- **Missing API keys**: verify `.env` is in the project root and keys are valid.
- **Gemini auth issues**: add `GOOGLE_API_KEY` in `.env`.
- **Scraping failures**: some sites block scraping or require JavaScript rendering.
- **Slow responses**: model/tool calls are network-dependent and may take time.

## Security

- Never commit `.env` or API keys.
- Rotate keys immediately if they are accidentally exposed.
