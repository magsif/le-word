# vision/render_board.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io
from PIL import Image, ImageDraw, ImageFont

def render_leword_board(guesses, word_length=5):
    fig, ax = plt.subplots(figsize=(word_length, len(guesses)))
    ax.axis("off")

    for row_idx, guess in enumerate(guesses):
        for col_idx, letter in enumerate(guess):
            if letter == '?':
                color = 'lightgray'
            elif letter.isupper():
                color = 'green'
            elif letter.islower():
                color = 'orange'
            else:
                color = 'white'

            rect = patches.Rectangle((col_idx, -row_idx), 1, 1, facecolor=color, edgecolor='black')
            ax.add_patch(rect)
            ax.text(col_idx + 0.5, -row_idx + 0.5, letter.upper(), ha='center', va='center', fontsize=16)

    ax.set_xlim(0, word_length)
    ax.set_ylim(-len(guesses), 1)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)



def render_leword_board2(feedback_list):
    """
    Render the LeWord board based on the list of feedback strings.
    Each feedback corresponds to one guess and contains characters or color hints.
    """
    cell_size = 50
    padding = 10
    word_length = len(feedback_list[0]) if feedback_list else 6
    rows = len(feedback_list)
    
    width = cell_size * word_length + padding * 2
    height = cell_size * rows + padding * 2
    
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    
    # Use a basic font, adjust path if necessary
    try:
        font = ImageFont.truetype("arial.ttf", 32)
    except IOError:
        font = ImageFont.load_default()

    for row, feedback in enumerate(feedback_list):
        for col, char in enumerate(feedback):
            x = padding + col * cell_size
            y = padding + row * cell_size
            
            # Draw cell background based on feedback character (example)
            if char == "G":  # Green - correct letter
                fill_color = "green"
            elif char == "Y":  # Yellow - wrong place
                fill_color = "yellow"
            else:
                fill_color = "lightgray"
            
            draw.rectangle([x, y, x + cell_size, y + cell_size], fill=fill_color, outline="black")
            
            # Draw letter in center
            w, h = draw.textsize(char, font=font)
            draw.text((x + (cell_size - w) / 2, y + (cell_size - h) / 2), char, fill="black", font=font)
    
    return img
