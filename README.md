# AI Local

AI Local contains two Python clients for experimenting with Gemini desktop chat and OpenAI-compatible local inference endpoints.

## Features

- Runs a Tkinter Gemini chat interface with local JSON conversation history.
- Creates, switches, and deletes local chat history files from the desktop UI.
- Streams responses from an OpenAI-compatible local server through a small CLI client.
- Supports configurable local server URL, API key placeholder, model name, and sample prompt through environment variables.

## Requirements

- Python 3.10 or newer.
- A Google API key for the Gemini desktop chat client.
- An OpenAI-compatible local inference server for `localAI.py`.
- Python packages listed in `requirements.txt`: `google-generativeai`, `openai`, `python-dotenv`, and `Pillow`.
- On Linux, a Tkinter-capable Python installation is required for the desktop GUI.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to a local .env file.
4. Configure the values needed for the client you want to run:

```env
OPENAI_BASE_URL=http://127.0.0.1:8000/v1
OPENAI_API_KEY=EMPTY
OPENAI_MODEL=your-local-model-name
GOOGLE_API_KEY=your-google-api-key
```

`localAI.py` also supports an optional `OPENAI_SAMPLE_PROMPT` value. If it is not set, the script uses its built-in sample prompt.

Before running `ai_main.py`, create a history folder in this repository if it does not already exist. The UI expects at least one JSON file in that folder when it starts.

## Usage

Run the Gemini desktop chat application:

```bash
python ai_main.py
```

Run the OpenAI-compatible local server client:

```bash
python localAI.py
```

## Project Structure

- `ai_main.py`: Tkinter Gemini chat client with local history file management.
- `localAI.py`: streaming CLI request against an OpenAI-compatible chat completions endpoint.
- `requirements.txt`: Python runtime dependencies.
- `.env.example`: sample configuration for Gemini and OpenAI-compatible local inference settings.
- `.gitignore`: excludes local environment files, virtual environments, cache files, and generated history outputs.

## 摘要

AI Local 收錄兩個本機 AI 實驗用 Python 程式。
`ai_main.py` 是使用 Gemini 的 Tkinter 桌面聊天介面，會把對話紀錄存成 JSON 檔。
`localAI.py` 是連接 OpenAI 相容本機推論服務的命令列範例，並以串流方式輸出回覆。
使用前需安裝 `requirements.txt`，並依 `.env.example` 建立本機環境檔。
若要啟動桌面聊天介面，執行 `python ai_main.py`；若要測試本機推論服務，執行 `python localAI.py`。
桌面聊天介面需要 `GOOGLE_API_KEY`，本機推論範例需要 `OPENAI_BASE_URL`、`OPENAI_API_KEY` 與 `OPENAI_MODEL`。
