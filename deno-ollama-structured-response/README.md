# deno-ollama-structured-response

This project contains a simple, Deno-based example of a local LLM invocation
(via Ollama) that produces a structured JSON response.

# Setup

1. Install [Deno](https://deno.com)
2. Install [ollama](https://ollama.com/)
3. Download any model, e.g `ollama pull llama3.1:8b`
4. Run script, providing the model pulled in step 3: `deno run --allow-net --allow-env --node-modules-dir=auto main.ts llama3.1:8b`
