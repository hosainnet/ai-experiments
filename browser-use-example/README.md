
# browser-use-example

A simple demonstration of using the `browser-use` library with Google's Gemini AI to automate web browsing tasks.

## Prerequisites

- Python 3.11 or higher
- Google Gemini API key

## Installation

1. Clone this repository
2. Install [uv](https://github.com/astral-sh/uv) package manager
3. Copy the environment file and add your API key:
   ```bash
   cp .env.example .env
   ```

4. Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/api-keys) and add it to your `.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Usage

Run the example script:

```bash
uv run main.py
```

The script will:
1. Initialize a Gemini Flash AI model
2. Create a browser automation agent with the task "Find the number 1 post on Show HN"
3. Execute the task using automated browser interactions
