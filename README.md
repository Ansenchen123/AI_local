# AI Local

This repository contains two local AI experiments:

- `ai_main.py`: a Tkinter chat UI that talks to Gemini and stores chat history locally.
- `localAI.py`: a small CLI client for an OpenAI-compatible local inference server.

## Requirements

- Python 3.10+
- A `.env` file based on `.env.example`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file and fill in the values you need:

- `GOOGLE_API_KEY` for `ai_main.py`
- `OPENAI_BASE_URL`, `OPENAI_API_KEY`, and `OPENAI_MODEL` for `localAI.py`

## Usage

Run the Gemini desktop chat app:

```bash
python ai_main.py
```

Run the local OpenAI-compatible client:

```bash
python localAI.py
```

## Notes

- Chat logs are written to the local `history/` folder and are ignored by git.
- Do not commit your real `.env` file or any generated history.
