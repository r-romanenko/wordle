from typing import List
import unittest

from wordle import GuessResult, GuessState, LetterState, WordleGame

class WordleCases(unittest.TestCase):
    def setUp(self) -> None:
        self.game: WordleGame = WordleGame()
        return super().setUp()

    def _assert_game_result(self, 
                            result: GuessResult, 
                            guess: str, 
                            letter_states: List[LetterState],
                            guesses_left: int, 
                            state: GuessState) -> None:
        
        if state != GuessState.INVALID_WORD:
            self.assertEqual(result.user_guess,  guess, "returned the word successfully")
            self.assertEqual(result.turns_remaining, guesses_left, "should have 5 turns remaining")
            self.assertEqual(result.state, state)
            for index, item in enumerate(result.letter_state):
                self.assertEqual(item, letter_states[index])

        result_string = result.get_state_string()

        if state == GuessState.GUESS_AGAIN:
            self.assertEqual(result_string, f"{guesses_left} turns left")
        elif state == GuessState.YOU_WON:
            self.assertEqual(result_string, "You Won!!")
        elif state == GuessState.YOU_LOST:
            self.assertEqual(result_string, f"You lost.  Word was {result.current_word}")
        else:
            self.assertEqual(result_string, "Not a word, try again.")

    def test_letter_state(self):
        self.game.start_new_game(5, "bikes")

        result = self.game.submit_guess_and_get_result("kites")
        self._assert_game_result(
            result, "kites", [LetterState.MATCH_LETTER, 
            LetterState.MATCH_PLACE, LetterState.NOT_FOUND, 
            LetterState.MATCH_PLACE, LetterState.MATCH_PLACE], 4, 
            GuessState.GUESS_AGAIN)
        guess_string = result.get_guess_string()
        guess_expected = "\x1b[33mk\x1b[m\x1b[32mi\x1b[m\x1b[mt\x1b[m\x1b[32me\x1b[m\x1b[32ms\x1b[m"
        self.assertEqual(guess_string, guess_expected)

    def test_multiple_letter(self):
        self.game.start_new_game(5, "where")

        result = self.game.submit_guess_and_get_result("earth")
        self._assert_game_result(
            result, "earth", [LetterState.MATCH_LETTER, 
            LetterState.NOT_FOUND, LetterState.MATCH_LETTER, 
            LetterState.NOT_FOUND, LetterState.MATCH_LETTER], 4, 
            GuessState.GUESS_AGAIN)

        result = self.game.submit_guess_and_get_result("plane")
        self._assert_game_result(
            result, "plane", [LetterState.NOT_FOUND, 
            LetterState.NOT_FOUND, LetterState.NOT_FOUND, 
            LetterState.NOT_FOUND, LetterState.MATCH_PLACE], 3, 
            GuessState.GUESS_AGAIN)

        result = self.game.submit_guess_and_get_result("eagle")
        self._assert_game_result(
            result, "eagle", [LetterState.MATCH_LETTER, 
            LetterState.NOT_FOUND, LetterState.NOT_FOUND, 
            LetterState.NOT_FOUND, LetterState.MATCH_PLACE], 2, 
            GuessState.GUESS_AGAIN)

    def test_win(self):
        self.game.start_new_game(6, "wolves")

        result = self.game.submit_guess_and_get_result("wolves")
        self._assert_game_result(
            result, "wolves", [LetterState.MATCH_PLACE, 
            LetterState.MATCH_PLACE, LetterState.MATCH_PLACE, 
            LetterState.MATCH_PLACE, LetterState.MATCH_PLACE, LetterState.MATCH_PLACE], 4, 
            GuessState.YOU_WON)

    def test_not_word(self):
        self.game.start_new_game(5, "bikes")

        result = self.game.submit_guess_and_get_result("zzzzz")
        self._assert_game_result(
            result, "bikes", [LetterState.MATCH_PLACE, 
            LetterState.MATCH_PLACE, LetterState.MATCH_PLACE, 
            LetterState.MATCH_PLACE, LetterState.MATCH_PLACE], 4, 
            GuessState.INVALID_WORD)

    def test_lose(self):
        self.game.start_new_game(5, "bikes")

        result = self.game.submit_guess_and_get_result("trail")
        result = self.game.submit_guess_and_get_result("steam")
        result = self.game.submit_guess_and_get_result("likes")
        result = self.game.submit_guess_and_get_result("fight")
        result = self.game.submit_guess_and_get_result("water")
        self._assert_game_result(
            result, "water", [LetterState.NOT_FOUND, 
            LetterState.NOT_FOUND, LetterState.NOT_FOUND, 
            LetterState.MATCH_PLACE, LetterState.NOT_FOUND], 0, 
            GuessState.YOU_LOST)

