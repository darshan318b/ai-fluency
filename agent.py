"""System 3: an AI agent. LLM + tools + loop."""
import json
import re
from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS

SYSTEM_PROMPT = (
    "You are a college fee assistant. Never guess a fee: always use get_course_fee. "
    "Use calculator for any arithmetic. Available course codes: CS101, AI202, DS303. "
    "If no tool is needed, answer directly."
)

def _clean_tool_name(name):
    """Some Groq models append junk like '<|channel|>commentary' to tool names.
    Strip anything that isn't a valid identifier character."""
    cleaned = re.sub(r"[^A-Za-z0-9_]", "", name)
    # If model returned something like 'calculatorcommentary', trim to known prefix
    for known in TOOL_FUNCTIONS:
        if cleaned.startswith(known):
            return known
    return cleaned

def agent(question, max_steps=6, verbose=True):
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}]

    for step in range(1, max_steps + 1):
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS, temperature=0)
        message = response.choices[0].message

        if not message.tool_calls:
            return message.content.strip()

        messages.append({
            "role": "assistant", "content": message.content or "",
            "tool_calls": [{"id": call.id, "type": "function",
                            "function": {"name": call.function.name,
                                         "arguments": call.function.arguments}}
                           for call in message.tool_calls]})

        for call in message.tool_calls:
            raw_name = call.function.name
            name = _clean_tool_name(raw_name)
            try:
                arguments = json.loads(call.function.arguments or "{}")
            except json.JSONDecodeError:
                arguments = {}
            function = TOOL_FUNCTIONS.get(name)
            result = function(**arguments) if function else f"Unknown tool: {raw_name}"
            if verbose:
                print(f"   step {step}: {name}({arguments}) -> {result}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

    return "Stopped: maximum steps reached without a final answer."

if __name__ == "__main__":
    banner("SYSTEM 3: AI AGENT")
    for question in QUESTIONS:
        print("Q:", question)
        print("A:", agent(question))
        print("-" * 70)
