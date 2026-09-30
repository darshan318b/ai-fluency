"""Day 3: the same ReAct loop with repeat, size, and budget guards."""
import json

from my_agent import SYSTEM_PROMPT
from my_tools import TOOL_FUNCTIONS, TOOLS
from config import MODEL, banner, client

MAX_TOOL_CHARS = 1500
CHAR_BUDGET = 30000
REPEAT_LIMIT = 3


def agent(question, max_steps=6, verbose=True):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    seen_calls = {}
    last_results = {}
    chars_sent = 0

    for step in range(1, max_steps + 1):
        chars_sent += sum(len(str(message.get("content", ""))) for message in messages)
        if chars_sent > CHAR_BUDGET:
            return f"Stopped: character budget exceeded ({chars_sent} sent)."

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
            arguments = {}
            signature = (name, call.function.arguments or "{}")
            try:
                arguments = json.loads(call.function.arguments or "{}")
                signature = (name, json.dumps(arguments, sort_keys=True))
                seen_calls[signature] = seen_calls.get(signature, 0) + 1
                if seen_calls[signature] >= REPEAT_LIMIT:
                    previous = last_results.get(signature, "No result was produced.")
                    return (
                        f"Stopped: {name} was requested {REPEAT_LIMIT} times with the same "
                        f"arguments and no progress was made. Last result: {previous[:200]}"
                    )

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
            last_results[signature] = result
            if len(result) > MAX_TOOL_CHARS:
                result = result[:MAX_TOOL_CHARS] + " ... [observation truncated]"
            if verbose:
                print(f"   step {step}: {name} -> {result[:120]}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

    return "Stopped: maximum steps reached without a final answer."


if __name__ == "__main__":
    banner("MY AGENT (guards on)")
    questions = [
        "Read notice.html and tell me the total fee for CS101 and AI202 after the merit scholarship.",
        "Read fees.html and tell me the fee for CS101.",
        "Read big.html and tell me how many students are listed.",
    ]
    for question in questions:
        print("\nQ:", question)
        print("A:", agent(question))