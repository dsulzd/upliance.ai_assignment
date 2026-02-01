# RPS-Bomb AI Judge

## Why I Structured the Prompt This Way

**1. Rules First, Then Workflow**  
The prompt starts with complete game rules before explaining what to do. This ensures the LLM has full context before making decisions, reducing hallucination of non-existent rules.

**2. Explicit Move Classification (VALID/INVALID/UNCLEAR)**  
Instead of binary valid/invalid, I added UNCLEAR for ambiguous inputs. This prevents the LLM from guessing when uncertain—safer for a judge role.

**3. Tool-Based State Management**  
The prompt instructs the LLM to call tools in order: `get_game_state → generate_bot_move → record_round_result → check_game_over`. This separates concerns: LLM judges, tools track state.

**4. Structured Output Format**  
Requiring a specific format ensures consistent, parseable responses and forces explanation of reasoning (builds user trust).

**5. Edge Case Examples in Prompt**  
Including examples like "rocc → rock" teaches lenient interpretation without hardcoding every variant in code.

---

## Failure Cases Considered

| Case | How Handled |
|------|-------------|
| Typos ("rocc", "scisor") | Prompt instructs lenient interpretation |
| Multiple moves ("rock paper") | Marked as UNCLEAR |
| Second bomb attempt | Marked as INVALID via state check |
| Empty/gibberish input | Marked as INVALID |
| Mixed signals ("rock... no, paper") | Marked as UNCLEAR |
| Case variations ("ROCK") | Explicitly case-insensitive |

---

## What I Would Improve Next

1. **Persistent State**: Add SQLite for state that survives restarts
2. **Multi-User Sessions**: Use ADK's `ToolContext.state` per user
3. **Evaluation Suite**: Add `adk eval` tests for edge cases
4. **Retry Logic**: Exponential backoff for API rate limits
