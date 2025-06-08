# LeWord Puzzle Solver — Multi-Agent AI System

This project implements a multi-agent AI system that plays the **LeWord** puzzle game (a Wordle-style word-guessing game). Two specialized agents—a **vision agent** and a **word agent**—collaborate to guess a hidden word based on feedback and visual cues.

The system uses structured tools, visual rendering, and Pydantic-based communication to simulate real-world AI agent collaboration.

---

## 📌 Features

- ✅ Two autonomous AI agents (vision + word decision)
- 🧰 Modular tool-based architecture
- 🎨 Visual board rendering processed by a vision model
- 📦 Structured state modeling using **Pydantic**
- 📡 Tool-calling and feedback-driven game loop
- 📈 Designed for experimentation with ChatGPT agents, vision models, and game state understanding

---

## 🧩 Project Structure
```
leword-ai/
│
├── game/
│ └── leword_game.py    # Game logic and feedback system
│ └── renderer.py       # Game rendering
│
├── tools/
│ └── game_tools.py # Tools: guess, hint, show_board_image
│
├── agents/
│ ├── chat_agent.py # OpenAI-compatible chat agent (ChatGPT)
│ ├── vision_agent.py # Vision model interface (mock or real)
│ └── word_agent.py # Word-choosing agent logic
│
├── vision/
│ └── render_board.py   # Converts game state to board images
│ └── vision_models.py 
│
├── models/
│ └── schemas.py # Pydantic models: GameState, GuessResult
│
├── notebooks/
│ └── leword_guesser.ipynb          # Alternate version using ChatGPT as primary agent
│ └── two_agents_working.ipynb      # Main notebook with vision & word agents
│
└── README.md # 📘 You are here
```

## Add .env

Add a .env file to your environment containing the OPENAI_API_KEY=sk..
