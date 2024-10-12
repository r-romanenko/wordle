import unittest
from wordle import WordList, GuessResult, GuessState, LetterState, WordleGame


class StudentTestCases(unittest.TestCase):

    def setUp(self) -> None:
        self.game: WordleGame = WordleGame()
        return super().setUp()
    
    def test_student_case(self):
        # if a letter appears later in the right place, 
        # don't make an earlier letter yellow as well

        self.game.start_new_game(5, "jolly")

        result = self.game.submit_guess_and_get_result("lolly")
        
        guess_string = result.get_guess_string()
        guess_expected = "\033[ml\033[m\033[32mo\033[m\033[32ml\033[m\033[32ml\033[m\033[32my\033[m"
        # Green \033[32m
        # Yellow \033[33m
        # Reset \033[m
        self.assertEqual(guess_string, guess_expected)
        
    


 