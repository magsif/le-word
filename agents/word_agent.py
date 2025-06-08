import random
from models.schemas import GameState

POSSIBLE_WORDS = [
    "mazda", "toyota", "subaru", "honda", "nissan", "suzuki", "lexus", "datsun"
]

def word_agent_decide_guess(vision_embedding, game_state: GameState) -> str:
    previous_guesses = {attempt.guess for attempt in game_state.attempts}
    remaining_words = [word for word in POSSIBLE_WORDS if word not in previous_guesses]

    if not remaining_words:
        return "mazda"  # fallback

    return random.choice(remaining_words)
