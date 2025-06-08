import json
from game.leword_game import LeWordGame
from tools.game_tools import guess, hint, render_board, available_tools
from agents.vision_agent import vision_agent_process_board
from agents.word_agent import word_agent_decide_guess
from models.schemas import GameState, GuessResult
from PIL import Image
import base64
from io import BytesIO
from vision.render_board import render_leword_board

# Create game instance
the_word = "subaru"
the_hint = "Japanese car brand."
game = LeWordGame(the_word, the_hint, 10)

# Initialize tools
functions = available_tools()

def decode_base64_image(img_b64: str) -> Image.Image:
    img_data = base64.b64decode(img_b64)
    return Image.open(BytesIO(img_data))

def run_turn(game):
    # Step 1: Render board and encode image
    if not game.attempts:
        dummy_board = [[' ']*len(game.target_word)]
        board_img = render_leword_board(dummy_board, len(the_word))        
    else:
        board_img = render_leword_board([list(attempt.feedback) for attempt in game.attempts], len(game.target_word))

    # Step 1: Render board and encode image
    vision_embedding = vision_agent_process_board(board_img)

    # Step 2: Create structured game state
    game_state = GameState(
        attempts=[
            GuessResult(
                guess=attempt.guess,
                feedback=attempt.feedback,
                correct=(attempt.guess.lower() == game.target_word.lower())
            )
            for attempt in game.attempts
        ],
        attempts_left=game.max_attempts - len(game.attempts),
        word_length=len(game.target_word)
    )       

    # Step 3: Word agent decides next guess based on vision + game state
    next_guess = word_agent_decide_guess(vision_embedding, game_state)

    # Step 4: Call guess tool with next_guess
    tool_response = guess(next_guess, game=game)
    print(f"Guess: {next_guess}, Feedback: {tool_response}")

    # Step 5: Check win condition
    game_over = tool_response.get("correct", False)

    return game_over

# Run game loop
for turn in range(game.max_attempts):
    print(f"Turn {turn+1}")
    game_over = run_turn(game)
    if game_over:
        print("🎉 Correct word guessed! Game over.")
        break
else:
    print("❌ Max attempts reached. Game over.")
