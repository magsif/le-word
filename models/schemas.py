from pydantic import BaseModel
from typing import List

class GuessResult(BaseModel):
    guess: str
    feedback: str
    correct: bool

class GameState(BaseModel):
    attempts: List[GuessResult]
    attempts_left: int
    word_length: int
