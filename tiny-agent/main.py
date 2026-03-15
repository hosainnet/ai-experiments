import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from skills import discover_skills
from tools import tools, available_functions, register_skill_tool

load_dotenv()

client = OpenAI(
    base_url=os.environ["BASE_URL"],
    api_key=os.environ["API_KEY"],
)


skills = discover_skills()
if skills:
    register_skill_tool(skills)


def agent_loop(user_message: str, max_iterations: int = 10) -> str:
    """Agent loop with error handling for production use."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use tools when needed. Do not reveal inner workings."},
        {"role": "user", "content": user_message},
    ]

    for i in range(max_iterations):
        try:
            response = client.chat.completions.create(
                model=os.environ["MODEL"],
                messages=messages,
                tools=tools,
                timeout=30,
            )
        except Exception as e:
            return f"API call failed: {e}"

        choice = response.choices[0]
        assistant_message = choice.message
        messages.append(assistant_message)

        if not assistant_message.tool_calls:
            # Stream the final response
            messages.pop()  # Remove the non-streamed response
            try:
                stream = client.chat.completions.create(
                    model=os.environ["MODEL"],
                    messages=messages,
                    tools=tools,
                    stream=True,
                    timeout=30,
                )
                full_response = ""
                for chunk in stream:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        print(delta.content, end="", flush=True)
                        full_response += delta.content
                print()
                return full_response
            except Exception as e:
                return f"Streaming failed: {e}"

        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            func = available_functions.get(function_name)
            if func:
                try:
                    result = func(function_args)
                except Exception as e:
                    result = json.dumps({"error": str(e)})
            else:
                result = json.dumps({"error": f"Unknown function: {function_name}"})

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

    return "Max iterations reached."

agent_loop("Hello")
agent_loop("What's the weather in San Francisco? Give me the temperature in Fahrenheit.")
