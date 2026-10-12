# Enrike Core Matrix (V1)

Autonomous browser-class companion engine powered by Open Interpreter.

## Setup Requirements
- Cloud environment running Python 3.10+
- Host deployment layer via FastAPI & Uvicorn WebSockets
- Environment variable configuration: `OPENROUTER_API_KEY`

## Ignition Command
`uvicorn app:app --host 0.0.0.0 --port $PORT`
