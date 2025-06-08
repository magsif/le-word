from enum import Enum
from dataclasses import dataclass

class LetterState(Enum):
    CORRECT = 1
    PRESENT = 2
    ABSENT = 3

# @dataclass
# class GuessResult:
#     word: str
#     states: list[LetterState]
#     is_correct: bool

@dataclass
class GuessResult:
    guess: str
    feedback: str
    score: int = 0
    correct: bool = False

class LeWordGame:
    def __init__(self, target_word, hint, max_attempts=6):
        self.target_word = target_word.lower()
        self.hint = hint
        self.max_attempts = max_attempts
        self.word_length = len(target_word)
        self.attempts: list[GuessResult] = []
        self.color_map = {
            LetterState.CORRECT: (0.0, 0.6, 0.0),
            LetterState.PRESENT: (0.8, 0.5, 0.0),
            LetterState.ABSENT: (0.3, 0.3, 0.3),
        }
        self.background_color = "black"

    def guess(self, guess):
        from collections import Counter

        answer = self.target_word
        guess = guess.lower()

        if len(guess) != self.word_length:
            guess_result = GuessResult(guess, "Invalid length of characters.", False)
            self.attempts.append(guess_result)
            return guess_result
    
        result = ['?'] * len(guess)
        answer_counts = Counter(answer)

        # First pass: correct positions
        for i in range(len(guess)):
            if guess[i] == answer[i]:
                result[i] = guess[i].upper()
                answer_counts[guess[i]] -= 1

        # Second pass: correct letters, wrong positions
        for i in range(len(guess)):
            if result[i] == '?':
                if guess[i] in answer_counts and answer_counts[guess[i]] > 0:
                    result[i] = guess[i]
                    answer_counts[guess[i]] -= 1
   
        feedback = ''.join(result)

        guess_result = GuessResult(guess, feedback, self.calculate_score(feedback), guess == self.target_word)
        #print(f"Guess: {word}, Result: {[s.name for s in guess_result.states]}, Correct: {guess_result.is_correct}")
        self.attempts.append(guess_result)
        return guess_result


    # def guess(self, word):
    #     word = word.lower()
    #     result = []
    #     used = [False] * self.word_length
    #     for i in range(self.word_length):
    #         if word[i] == self.target_word[i]:
    #             result.append(LetterState.CORRECT)
    #             used[i] = True
    #         else:
    #             result.append(None)
    #     for i in range(self.word_length):
    #         if result[i] is None:
    #             if word[i] in self.target_word and not used[self.target_word.index(word[i])]:
    #                 result[i] = LetterState.PRESENT
    #                 used[self.target_word.index(word[i])] = True
    #             else:
    #                 result[i] = LetterState.ABSENT

    #     guess_result = GuessResult(word, result, word == self.target_word)
    #     #print(f"Guess: {word}, Result: {[s.name for s in guess_result.states]}, Correct: {guess_result.is_correct}")
    #     self.attempts.append(guess_result)
    #     return guess_result

    def is_game_over(self):
        return len(self.attempts) >= self.max_attempts or (self.attempts and self.attempts[-1].is_correct)

    def get_hint(self):
        return self.hint

    def get_final_score(self):
        return max(0, 100 - 10 * len(self.attempts))

    def score(self):
        return self.get_final_score()
    
    def calculate_score(self, feedback: str) -> int:
        score = 0
        for ch in feedback:
            if ch.isupper():
                score += 10
            elif ch.islower():
                score += 5
            elif ch == '?':
                score -= 10
        score = max(0, min(100, score))
        return score

    def state(self):
        return [(gr.guess, gr.feedback) for gr in self.attempts]

    def instructions(self):
        return f"""
            Let's play a word-guessing game called LeWord!
            I will give you a hint, and you have to guess the secret word.

            IMPORTANT:
            - You must guess words that are EXACTLY {self.word_length} letters long.
            - Any guess shorter or longer than {self.word_length} letters will be rejected, and you will lose an attempt.
            - Do NOT guess any invalid-length word, even once.

            Example valid guess: "plato" (5 letters)
            Example invalid guess: "caesar" (6 letters)

            You have {self.max_attempts} attempts to guess the correct word.
            The word length is {self.word_length} characters.

            After each guess, you will receive feedback using a string of {self.word_length} characters:
            - An uppercase letter means that letter is correct and in the correct position.
            - A lowercase letter means that letter is in the word but in the wrong position.
            - A '?' means the letter is not in the word at all.

            If the secret word is "grape" and you guess "apple", the feedback would be "ap??E" because:
            - 'a' (lowercase) means 'a' is in the word but not in that position.
            - 'p' (lowercase) means 'p' is in the word but not in that position.
            - The second 'p' does not appear twice in the word, so it gets a '?'.
            - 'l' is not in the word, so it gets a '?'.
            - 'E' (uppercase) means 'e' is in the correct position.

            If you guess the word correctly (all uppercase letters matching the word), you win!

            If you receive feedback of a character that is not uppercase or lowercase, it means your guess was invalid.

            If you receive character in lower case, it means that letter is in the word but in the wrong position and you must try again with a different position for that letter.

            You must NOT repeat any previously guessed word, whether it was invalid or incorrect.
            Repeating any guess will cause you to lose an extra attempt.

            Each guess you make will receive a score between 0 and 100:
            - 100 means a perfect guess (correct word).
            - Higher score means your guess is closer to the correct word.
            - Use the score to help you make better guesses.

            Here's your hint: {self.hint}.
        """

    
    def reset(self, target_word=None, hint=None):
        self.reset_game(target_word, hint)

    def tips(self):
        return """
            You can use the following tools:
            - 'guess' to make a guess
            - 'get' to ask for a clue
        """
    
    def pretty_last_guess(self):
        if not self.attempts:
            return "No guesses yet."
        return self.attempts[-1].result
