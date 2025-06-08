import openai
from dotenv import load_dotenv
import os

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def init_chat_agent(game):
    """
    Initializes the system prompt messages for the ChatGPT agent,
    embedding the game instructions and available tools descriptions.
    """
    return [
        {
            "role": "system",
            "content": f"""
                Instructions:
                {game.instructions()}

                Tips:
                {game.tips()}
            """
        }
    ]

def ask_chat_agent(messages, functions):
    """
    Sends messages and function definitions to the OpenAI chat completion API,
    with automatic function call selection enabled.
    """

    print("Messages sent to OpenAI API:")
    for msg in messages:
        print(msg)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    # Return the full response object or just the message part as needed
    return response

def parse_response(response):
    try:
        tool_call = response.choices[0].message.tool_calls[0]
        return tool_call.function.name, tool_call.function.arguments
    except Exception as e:
        return None, None