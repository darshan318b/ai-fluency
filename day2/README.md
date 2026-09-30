# Day 2 Lab - Reasoning Techniques

This lab compares reasoning approaches using the shared Day 1 agent configuration.

- `cot_compare.py` compares direct answers with chain-of-thought prompting.
- `self_consistancy.py` samples multiple chain-of-thought answers and selects the majority.
- `react_trace.py` prints the agent's ReAct tool-use trace.

Install this lab's dependencies with `pip install -r requirements.txt`, configure your model provider in `.env`, then run a script with `python cot_compare.py`, `python self_consistancy.py`, or `python react_trace.py` from this folder.