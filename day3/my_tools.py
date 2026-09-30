"""Day 3 tools: a safe calculator and a local/web page reader."""
import ast
import html
import operator
import re
from pathlib import Path
from urllib.parse import urlparse

LAB_DIR = Path(__file__).resolve().parent
_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}
_TAG = re.compile(r"<(script|style)\b[^>]*>.*?</\1\s*>|<!--.*?-->|<[^>]+>", re.I | re.S)
_SPACES = re.compile(r"\s+")


def _evaluate(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("Exponent magnitude must be 100 or less")
        return _OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Unsupported expression")


def calculator(expression: str) -> str:
    """Evaluate arithmetic without executing Python code."""
    try:
        if len(expression) > 256:
            raise ValueError("Expression is too long")
        parsed = ast.parse(expression, mode="eval")
        return str(_evaluate(parsed.body))
    except Exception as error:
        return f"Calculator error: {error}. Use only numbers and + - * / ** ( )."


def _visible_text(raw: str) -> str:
    return _SPACES.sub(" ", html.unescape(_TAG.sub(" ", raw))).strip()


def read_webpage(url: str, max_chars: int = 2000) -> str:
    """Read an HTTP(S) page or a local HTML/text file inside the Day 3 folder."""
    try:
        parsed = urlparse(url)
        if parsed.scheme in ("http", "https") and parsed.netloc:
            import requests

            response = requests.get(
                url,
                timeout=10,
                headers={"User-Agent": "AgenticAI-Lab/1.0"},
            )
            response.raise_for_status()
            raw = response.text
        elif not parsed.scheme:
            path = Path(url)
            if not path.is_absolute():
                path = LAB_DIR / path
            path = path.resolve()
            try:
                path.relative_to(LAB_DIR)
            except ValueError:
                return "Read error: local files must be inside the Day 3 folder."
            if path.suffix.lower() not in (".html", ".htm", ".txt"):
                return "Read error: local files must use .html, .htm, or .txt."
            if not path.is_file():
                return f"Read error: '{url}' is not a URL and no such file exists."
            raw = path.read_text(encoding="utf-8", errors="ignore")
        else:
            return "Read error: use an http(s) URL or a local .html/.htm/.txt file."
    except Exception as error:
        return f"Read error: {type(error).__name__}: {error}"

    text = _visible_text(raw)
    if not text:
        return "Read error: the page contained no readable text."
    if len(text) > max_chars:
        return text[:max_chars] + f" ... [truncated, {len(text)} characters total]"
    return text


TOOL_FUNCTIONS = {"calculator": calculator, "read_webpage": read_webpage}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate arithmetic using + - * / ** and parentheses.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Arithmetic expression, e.g. (12000 + 18000) * 0.9",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_webpage",
            "description": "Read an HTTP(S) page or local HTML/text file and return visible text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "HTTP(S) URL or local file name such as notice.html",
                    }
                },
                "required": ["url"],
            },
        },
    },
]


if __name__ == "__main__":
    print(calculator("(12000 + 18000) * 0.9"))
    print(calculator("2 ** 10"))
    print(calculator("import os"))
    print(read_webpage("notice.html")[:200])
    print(read_webpage("no_such_file.html"))