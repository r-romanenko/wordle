
from wordle import WordleGame

game = WordleGame()
game.start_new_game(5)
while game.has_more_guesses() and not game.has_won:
    guess = input("Enter a word\n")
    result = game.submit_guess_and_get_result(guess)
    print(result.get_guess_string())
    print(result.get_state_string())