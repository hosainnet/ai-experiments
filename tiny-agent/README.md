# Tiny Agent

A minimal tool-calling agent loop using Ollama and the OpenAI-compatible API. The agent can chain multiple tool calls to answer a question — for example, fetching weather data and then converting the temperature.

## How it works

1. A user message is sent to the LLM (llama3.1:8b via Ollama)
2. The model decides which tools to call and with what arguments
3. Tool results are fed back into the conversation
4. Steps 2–3 repeat until the model produces a final text response

## Tools

- **get_weather** — Returns simulated weather data for a location
- **convert_temperature** — Converts between Celsius and Fahrenheit

## Setup

Requires [Ollama](https://ollama.com/) running locally with the `llama3.1:8b` model:

```sh
ollama pull llama3.1:8b
```

Copy the example env file and adjust as needed:

```sh
cp .env.example .env
```

| Variable   | Description                        | Default                          |
|------------|------------------------------------|----------------------------------|
| `BASE_URL` | OpenAI-compatible API base URL     | `http://localhost:11434/v1/`     |
| `API_KEY`  | API key for the provider           | `ollama`                         |
| `MODEL`    | Model name to use                  | `llama3.1:8b`                     |

## Run

```sh
uv run main.py
```

## Attribution

Based on [Build an AI Agent Loop in 50 Lines of Python](https://dev.to/klement_gunndu/build-an-ai-agent-loop-in-50-lines-of-python-59jk) by Klement Gunndu.
