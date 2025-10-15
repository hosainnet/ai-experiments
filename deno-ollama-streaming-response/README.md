# Deno Ollama Streaming Response

A simple Deno HTTP server that demonstrates streaming responses from Ollama using LangChain.

## Description

This project creates an HTTP server that uses the Ollama language model to generate streaming text responses. When you make a request to the server, it sends a predefined question to the Ollama model and streams the response back in real-time.

## Features

- Streaming responses from Ollama using LangChain
- Simple HTTP server built with Deno
- Uses `llama3.2:latest` model by default

## Prerequisites

- [Deno](https://deno.land/) installed
- [Ollama](https://ollama.ai/) installed and running
- The `llama3.2:latest` model pulled in Ollama (`ollama pull llama3.2:latest`)

## Usage

1. Start Ollama service:

```bash
ollama serve
```

2. Run the Deno server:
```bash
deno run --allow-net --allow-env --node-modules-dir=auto main.ts
```

3. Make a request to the server:
```bash
curl http://localhost:8000
```

The server will respond with a streaming text answer to "Give me a 10000 word story about the galaxy"

Note that the response will be chunked rather than blocking the whole request until the full LLM response is generated.

## Configuration

To change the model or input text, modify the following in `main.ts`:

- `model: "llama3.2:latest"` - Change to use a different Ollama model
- `const inputText = "..."` - Change the question being asked

## Dependencies

- `@langchain/ollama` - LangChain integration for Ollama
