import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from PIL import Image
import base64
from game.leword_game import LetterState, GuessResult

# Define a color map for tiles
COLOR_MAP = {
    LetterState.CORRECT: [0.108, 0.478, 0.235],  # Green
    LetterState.PRESENT: [0.682, 0.584, 0.208],  # Yellow
    LetterState.ABSENT: [0.15, 0.15, 0.15],      # Dark gray
}
BACKGROUND_COLOR = [0.1, 0.1, 0.1]  # Slightly darker than ABSENT

def render_game_image(game) -> Image.Image:
    """Render the current game state as a PIL image."""
    word_length = game.word_length
    max_attempts = game.max_attempts
    attempts = game.attempts

    # Create a blank grid
    grid = np.full((max_attempts, word_length, 3), COLOR_MAP[LetterState.ABSENT])

    for i, attempt in enumerate(attempts):
        for j, state in enumerate(attempt.states):
            grid[i, j] = COLOR_MAP[state]

    # Plot setup
    fig, ax = plt.subplots(figsize=(word_length * 0.8, max_attempts * 0.8))
    ax.set_facecolor(BACKGROUND_COLOR)
    fig.patch.set_facecolor(BACKGROUND_COLOR)

    ax.imshow(grid, aspect='equal')

    # Add text (letters)
    for i in range(max_attempts):
        for j in range(word_length):
            if i < len(attempts):
                letter = attempts[i].word[j].upper()
                ax.text(j, i, letter, ha='center', va='center',
                        color='white', fontsize=16, weight='bold')

    # Draw grid lines
    for i in range(max_attempts + 1):
        ax.axhline(i - 0.5, color='gray', linewidth=0.5)
    for j in range(word_length + 1):
        ax.axvline(j - 0.5, color='gray', linewidth=0.5)

    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    
    # Convert to PIL Image
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

def render_game_state(game):
    grid = np.zeros((game.max_attempts, game.word_length, 3))
    for i, attempt in enumerate(game.attempts):
        for j, state in enumerate(attempt.states):
            grid[i, j] = game.color_map[state]

    fig, ax = plt.subplots(figsize=(game.word_length * 0.8, game.max_attempts * 0.8))
    ax.set_facecolor(game.background_color)
    ax.imshow(grid)

    for i, attempt in enumerate(game.attempts):
        for j, letter in enumerate(attempt.word):
            ax.text(j, i, letter.upper(), ha='center', va='center', fontsize=14, color='white')

    ax.axis('off')
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return Image.open(buf)

def as_base64_image(game):
    image = render_game_state(game)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    return f"data:image/png;base64,{base64.b64encode(img_bytes).decode()}"