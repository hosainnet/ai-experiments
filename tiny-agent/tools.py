import json

from skills import SkillRecord, activate_skill


# The actual functions your tools call
def get_weather(location: str) -> str:
    """Simulated weather lookup."""
    weather_data = {
        "San Francisco, CA": {"temp": 15, "unit": "celsius", "condition": "foggy"},
        "New York, NY": {"temp": 22, "unit": "celsius", "condition": "sunny"},
        "London, UK": {"temp": 11, "unit": "celsius", "condition": "rainy"},
    }
    data = weather_data.get(location, {"temp": 20, "unit": "celsius", "condition": "unknown"})
    return json.dumps(data)

def convert_temperature(value: float, from_unit: str, to_unit: str) -> str:
    """Convert between celsius and fahrenheit."""
    if from_unit == "celsius" and to_unit == "fahrenheit":
        result = (value * 9 / 5) + 32
    elif from_unit == "fahrenheit" and to_unit == "celsius":
        result = (value - 32) * 5 / 9
    else:
        result = value
    return json.dumps({"value": round(result, 1), "unit": to_unit})

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather in a given location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state, e.g. San Francisco, CA"
                    }
                },
                "required": ["location"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_temperature",
            "description": "Convert a temperature value between celsius and fahrenheit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {"type": "number", "description": "Temperature value to convert"},
                    "from_unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    "to_unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["value", "from_unit", "to_unit"],
                "additionalProperties": False
            }
        }
    }
]

# Map function names to actual Python functions
available_functions = {
    "get_weather": lambda args: get_weather(args["location"]),
    "convert_temperature": lambda args: convert_temperature(
        args["value"], args["from_unit"], args["to_unit"]
    ),
}


def register_skill_tool(skills: dict[str, SkillRecord]) -> None:
    """Register the activate_skill tool with discovered skill names."""
    skill_names = list(skills.keys())
    tools.append({
        "type": "function",
        "function": {
            "name": "activate_skill",
            "description": "Activate a skill to load specialized instructions. Use this when the user's request matches a skill's description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "enum": skill_names,
                        "description": "Skill to activate. Available: "
                        + ", ".join(
                            f"{s.name} ({s.description})" for s in skills.values()
                        ),
                    }
                },
                "required": ["name"],
                "additionalProperties": False,
            },
        },
    })
    available_functions["activate_skill"] = lambda args: activate_skill(args["name"], skills)

