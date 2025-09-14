import os
from dotenv import load_dotenv
import openai
from tools.tools import get_current_time, get_weather
import json

# Load environment variables from .env file
load_dotenv()

SYSTEM_PROMPT = """
You are Aditya, a dependable and precise AI assistant. 
Your responsibility is to resolve user queries with accuracy, clarity, and professionalism.

Guidelines:
- Always provide clear, concise, and correct responses in plain text only (no Markdown formatting like **bold** or *italics*).  
- When a query involves fetching the current time, use the tool: get_current_time.  
- When a query involves fetching the weather, use the weather tool.  
- For other queries requiring external data or computation, check the available tools.  
- If no relevant tool is available or the requested information cannot be reliably determined, politely apologize and clearly state that you cannot provide the answer. Never generate false or misleading information.  

Your goal is to ensure trust, accuracy, and helpfulness in every interaction.
"""


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Returns the current server time in ISO format.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a given location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The name of the location (city, address, etc.)"}
                },
                "required": ["location"]
            }
        }
    }
]

tool_functions = {
    "get_current_time": get_current_time,
    "get_weather": get_weather
}

class OpenAIClient:
    """Client for interacting with the OpenAI API using the official SDK."""
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided or set in the environment variable 'OPENAI_API_KEY'.")
        openai.api_key = self.api_key

    def chat(self, prompt: str, model: str = "gpt-4o-mini", **kwargs):
        completion = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": str(prompt)}
            ],
            tools=tools,
            tool_choice="auto",
            **kwargs
        )
        message = completion.choices[0].message
        # If tool call is present, execute the tool and call chat again with tool response
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_func = tool_functions.get(tool_name)
            if tool_func:
                # Parse arguments for the tool function
                args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
                tool_result = tool_func(**args)
                tool_result_str = json.dumps(tool_result)
                # Call chat again with tool response as assistant message
                completion2 = openai.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": str(prompt)},
                        {"role": "assistant", "content": None, "tool_calls": [tool_call]},
                        {"role": "tool", "tool_call_id": tool_call.id, "name": tool_name, "content": tool_result_str}
                    ],
                    tools=tools,
                    tool_choice="none"
                )
                return completion2.choices[0].message
        return message
