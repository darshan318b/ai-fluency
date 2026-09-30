# Day 3 Failure Log

The loop and guard checks below used stubbed model responses, so they made no provider calls. Real-provider wording and turn counts can vary. The large-prompt failure is not triggered automatically.

| Test | Setup | Expected observation | Recorded run |
|---|---|---|---|
| Repeating loop | Stub the model to request `read_webpage` for the same missing file on every turn | Unguarded agent reached its six-turn limit after 6 mocked model calls. Fixed agent stopped on the third identical request after 3 mocked calls. | Verified offline; no provider calls |
| Hallucinated tool, safe lookup | Stub a `send_email` request | Safe `.get()` returned an `Unknown tool` observation; the next mocked response completed normally. | Verified offline; no provider calls |
| Hallucinated tool, unsafe lookup | Temporarily replace `.get(name)` with `[name]` | The unknown tool raises `KeyError`; restore `.get(name)` immediately. | Not run; unsafe variant intentionally avoided |
| Context overflow | Generate `big.html`; raise reader `max_chars` only in a controlled local experiment | A provider may reject or slow down on the oversized prompt. Restore `max_chars=2000` immediately. | Not run; avoided hosted-provider cost risk |

Additional offline checks verified malformed tool JSON returns an error observation, the character budget stops before a model call, and a long tool result is truncated. `my_tools.py` validates arithmetic, refusal of Python code, HTML cleanup, local truncation, and missing-file messages without calling an LLM.