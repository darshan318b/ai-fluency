# Day 3 Observation Table

The tool-call counts below are the expected counts from the task requirements. Model-turn counts and wording vary by provider; fill those from your run rather than treating them as fixed.

## Part C: Two Tools, One Question

| Question | Expected tool calls | Expected result | Actual model turns / notes |
|---|---:|---|---|
| Merit scholarship total for CS101 and AI202 | 2: read + calculate | Rs. 27,000 | Record after running |
| Hostel student, all three courses plus lab charges | 3: read + calculate + calculate | Rs. 49,500 | Record after running |
| 15% of AI202 fee | 2: read + calculate | Rs. 2,700 | Record after running |
| One-line welcome message | 0 | Direct response; no tools | Record after running |

## Part D: Failure Modes

| Failure | Expected unguarded behavior | Guarded behavior | Actual result / measured cost |
|---|---|---|---|
| Repeated missing-file call | Repeats until the six-turn limit if the model retries the read | Stops on the third identical tool request | Record provider-dependent turns |
| Unknown tool | Safe `.get()` returns an `Unknown tool` observation; unsafe `[...]` raises `KeyError` | Safe registry lookup stays in use | Record only if the model requests an unknown tool |
| Large page | Removing truncation may create an oversized prompt or provider error | Reader truncation, per-observation cap, and character budget limit input | Do not run the untruncated hosted-provider experiment; record only in a controlled local setup |

## Chosen Limits

| Setting | Value | Reason |
|---|---:|---|
| `max_steps` | 6 | Bounds the unguarded loop and allows several tool rounds |
| Reader `max_chars` | 2000 | Limits one page before it reaches the model |
| `MAX_TOOL_CHARS` | 1500 | Caps each tool observation in the guarded agent |
| `CHAR_BUDGET` | 30000 | Stops when cumulative message characters sent across turns grow too large |
| Repeat threshold | 3 | Stops a repeated tool request while allowing a retry |

## Answer Checks

- Scholarship: `(12000 + 18000) * 0.9 = 27000`.
- Hostel total: `12000 + 18000 + 15000 + 4500 = 49500`.
- AI202 discount: `18000 * 0.15 = 2700`.