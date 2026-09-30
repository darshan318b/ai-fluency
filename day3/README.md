# Day 3 Lab - ReAct Agent Failure Modes

Build a ReAct loop in plain Python with a safe calculator and a local/web page reader. Compare an unguarded agent with one that detects repeated calls, truncates tool output, and enforces a character budget.

## Setup

Day 3 reuses the provider configuration in `../day1/config.py` and the `.env` in `day1`. Install Day 3's dependencies into the Day 1 environment:

```powershell
..\day1\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run commands from this folder with the Day 1 interpreter, for example:

```powershell
..\day1\.venv\Scripts\python.exe my_tools.py
..\day1\.venv\Scripts\python.exe my_agent.py
..\day1\.venv\Scripts\python.exe my_agent_fixed.py
```

`my_tools.py` and the local file exercises work without internet access. `requests` is only used for HTTP/HTTPS URLs.

## Lab Files

- `my_tools.py`: tool functions, registry, JSON schemas, and local smoke examples.
- `my_agent.py`: the ReAct loop without repeat, observation-size, or character-budget guards.
- `my_agent_fixed.py`: the same loop with those three guards.
- `notice.html`: source document for fee questions.
- `make_big_page.py`: creates `big.html` for the optional context-size experiment.
- `observations.md` and `failure_log.md`: expected results and a place to record provider-dependent measurements.

The missing-file loop can be exercised without editing the script:

```powershell
..\day1\.venv\Scripts\python.exe my_agent.py --question "Read fees.html and tell me the fee for CS101."
```

The unguarded loop is capped at six model turns. Do not raise that limit for the large-page test on a hosted provider: it can send large prompts repeatedly. Keep the reader's default `max_chars=2000` outside that experiment, and restore it immediately after testing.