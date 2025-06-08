from game.leword_game import LeWordGame, GuessResult
from vision.render_board import render_leword_board
from io import BytesIO
import base64

# def guess(guess: str, game: LeWordGame):
#     result = game.guess(guess)
#     return f"{game.pretty_last_guess()}  (Score: {game.calculate_score(game.pretty_last_guess())}, Correct: {result.is_correct})"

def guess(guess: str, game: LeWordGame):
    result = game.guess(guess)

    return {        
        "guess": result.guess,
        "feedback": result.feedback,
        "score": result.score,
        "correct": result.correct
    }

def hint(game: LeWordGame) -> str:
    hint = game.get_hint()
    if hint:
        return f"Hint: {hint}"
    else:
        return "No hint available."
    
def show_board_image(game):
    """
    Render the current game board and return it as a base64-encoded PNG image.
    """
    feedbacks = [list(result.feedback) for result in game.attempts]
    word_length = len(game.target_word)

    img = render_leword_board(feedbacks, word_length)

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    return {
        "image_base64": img_base64,
        "description": f"{len(game.attempts)} attempts made on a word of length {word_length}."
    }


def available_tools():
    """
    Returns the list of functions in the format expected by OpenAI chat completions.
    NOTE: each function dict must have keys: name, description, parameters (no extra nesting).
    """
    return [
        {
            "name": "guess",
            "description": "Make a guess in the LeWord game by providing a guess word.",
            "parameters": {
                "type": "object",
                "properties": {
                    "guess": {"type": "string", "description": "The guessed word"}
                },
                "required": ["guess"]
            }
        },
        {
            "name": "hint",
            "description": "Get a hint for the current LeWord game.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "show_board_image",
            "description": "Return a visual rendering (as base64) of the current game board.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }        
    ]

def render_board(game):
    # Render PIL Image of current game state
    img = render_leword_board([f for _, f in game.attempts])

    # Convert to base64 string so it can be passed easily as JSON
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return {"image_base64": img_str}

def reveal_letter(index: int, game: LeWordGame) -> dict:
    if index < 0 or index >= len(game.answer):
        return {"feedback": "Invalid index", "letter": None}
    return {"feedback": f"The letter at position {index} is revealed.", "letter": game.answer[index]}

