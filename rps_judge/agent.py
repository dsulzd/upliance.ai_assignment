import random
from pathlib import Path
from google.adk.agents import Agent

PROMPT = (Path(__file__).parent / "prompt.txt").read_text()

state = {"round": 1, "user": 0, "bot": 0, "user_bomb": False, "bot_bomb": False}


def get_game_state() -> dict:
    return state.copy()


def generate_bot_move() -> dict:
    if not state["bot_bomb"] and random.random() < 0.15:
        return {"bot_move": "bomb"}
    return {"bot_move": random.choice(["rock", "paper", "scissors"])}


def record_round_result(user_move: str, bot_move: str, winner: str) -> dict:
    if winner == "user": state["user"] += 1
    elif winner == "bot": state["bot"] += 1
    if user_move.lower() == "bomb": state["user_bomb"] = True
    if bot_move.lower() == "bomb": state["bot_bomb"] = True
    state["round"] += 1
    return {"recorded": True, "score": f"User {state['user']} - Bot {state['bot']}"}


def check_game_over() -> dict:
    if state["round"] > 5:
        if state["user"] > state["bot"]: result = "User Wins!"
        elif state["bot"] > state["user"]: result = "Bot Wins!"
        else: result = "Draw!"
        return {"game_over": True, "result": result}
    return {"game_over": False}


def reset_game() -> dict:
    state.update({"round": 1, "user": 0, "bot": 0, "user_bomb": False, "bot_bomb": False})
    return {"reset": True}


root_agent = Agent(
    name="rps_judge",
    model="gemini-2.0-flash",
    instruction=PROMPT,
    tools=[get_game_state, generate_bot_move, record_round_result, check_game_over, reset_game],
)
