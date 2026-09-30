"""Day 3: a plain ReAct agent loop without the three resource guards."""
import argparse
import json
import sys
from pathlib import Path

DAY1_DIR = Path(__file__).resolve().parent.parent / "day1"
sys.path.insert(0, str(DAY1_DIR))

from config import MODEL, banner, client
from my_tools import TOOL_FUNCTIONS, TOOLS

SYSTEM_PROMPT = (
    "You are a college assistant. Use read_webpage to read any page or file the user "
    "mentions, and use calculator for every arithmetic step. Never guess a number that "
    "should come from a page. If no tool is needed, answer directly."
)


def agent(question, max_steps=6, verbose=True):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for step in range(1, max_steps + 1):
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS, temperature=0
        )
        message = response.choices[0].message
        if not message.tool_calls:
            return (message.content or "").strip()

        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments,
                    },
                }
                for call in message.tool_calls
            ],
        })

        for call in message.tool_calls:
            name = call.function.name
            try:
                arguments = json.loads(call.function.arguments or "{}")
                function = TOOL_FUNCTIONS.get(name)
                if function is None:
                    result = f"Unknown tool: {name}. Available: {list(TOOL_FUNCTIONS)}"
                else:
                    result = function(**arguments)
            except json.JSONDecodeError as error:
                result = f"Argument error: {error}. Send valid JSON."
            except Exception as error:
                result = f"Tool error: {type(error).__name__}: {error}"

            result = str(result)
            if verbose:
                print(f"   step {step}: {name} -> {result[:120]}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

    return "Stopped: maximum steps reached without a final answer."


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the unguarded Day 3 ReAct agent.")
    parser.add_argument(
        "--question",
        default="Read notice.html and tell me the total fee for CS101 and AI202 after the merit scholarship.",
    )
    args = parser.parse_args()
    banner("MY AGENT (no guards)")
    print("Q:", args.question)
    print("A:", agent(args.question))