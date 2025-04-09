# Web Research AI Agent

This AI agent is designed to perform web research about technologies, products, or companies using LangChain/LangGraph, DuckDuckGoRun and OpenAI's API.

## Setup

1. Create a `.env` file in the root directory with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script:
```bash
python web_researcher.py "your research query"
```

The agent will:
1. Search the web for relevant information
2. Process and analyze the findings
3. Generate a comprehensive research report
