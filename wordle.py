from cgi import test
from enum import Enum
from mimetypes import guess_all_extensions
from operator import truediv
from sys import getfilesystemencodeerrors
from typing import List, Dict
import random

class GuessState(Enum):
    UNKNOWN = 0
    INVALID_WORD = 1
    GUESS_AGAIN = 2
    YOU_LOST = 3
    YOU_WON = 4

class LetterState(Enum):
    MATCH_LETTER = 0
    MATCH_PLACE = 1
    NOT_FOUND = 2

class TextColor:
    GREEN =  '\033[32m'
    YELLOW =  '\033[33m'
    RESET =  '\033[m'
# END CONSTANTS


class GuessResult():
    
    
    def __init__(self, guess:str, turns_remaining:int):
        self.user_guess:str = guess
        self.turns_remaining:int = turns_remaining
        self.state:GuessState = GuessState.UNKNOWN
        self.letter_state:List[LetterState] = []
        self.current_word:str = "None"

    def get_state_string(self) -> str:
        if (self.state == GuessState.GUESS_AGAIN):
            return f"{self.turns_remaining} turns left"
        elif (self.state == GuessState.YOU_WON):
            return "You Won!!"
        elif (self.state == GuessState.YOU_LOST):
            return f"You lost.  Word was {self.current_word}"
        return "Not a word, try again."
   
    def get_guess_string(self) -> str:
        colored_string = ""
        for x in range(len(self.letter_state)):
            if (self.letter_state[x] == LetterState.MATCH_LETTER):
                colored_string += f"{TextColor.YELLOW}{self.user_guess[x]}{TextColor.RESET}"
            elif (self.letter_state[x] == LetterState.MATCH_PLACE):
                colored_string += f"{TextColor.GREEN}{self.user_guess[x]}{TextColor.RESET}"
            else:
                colored_string += f"{TextColor.RESET}{self.user_guess[x]}{TextColor.RESET}"
        return colored_string


# A "dictionary" of words that you can use for the game
# selects and verifies whether words are words of the length being tracked
class WordList():
   
    def __init__(self) -> None:
        # load words from file;
        with open("words.txt", "r", encoding="utf-8") as file:
            self._words = [line.rstrip() for line in file]
            # init other attributes here
            self._word_length:int = 0
            self._active_words:List[str] = []


   
    # Sets the length of the words that we are looking for and adds all words 
    # of that length to _active_words
    def set_active_word_length(self, length:int) -> None:
        self._word_length = length
        self._active_words.clear()
        for x in self._words:
            if (len(x) == self._word_length):
                self._active_words.append(x)

    # Checks to see if word is a valid word of the length we are looking for.
    def is_valid_word(self, word:str) -> bool:
        for x in self._active_words:
            if x == word:
                return True
        return False
    
    # Picks a random word of the current active word length
    def pick_random_word(self) -> str:
        return self._active_words[random.randrange(0, len(self._active_words))]

MAX_GUESSES = 5


# Manages the gameplay logic for Wordle.
class WordleGame():

    def __init__(self) -> None:
        self._turns_remain:int = MAX_GUESSES
        self._target:str = ""
        self._word_list:WordList = WordList()
        self.has_won:bool = False
        

    # Checks to see if you can continue to guess words
    def has_more_guesses(self) -> bool:
        return self._turns_remain > 0

    # Starts a new game of Wordle using words of the given length
    def start_new_game(self, length:int, test_word:str = None) -> None:
        self.__init__()
        self.has_won = False
        self._word_list.set_active_word_length(length)

        # picks the word you're guessing
    
        if test_word == None:
            self._target = self._word_list.pick_random_word() # instead of using test_word
        else:
            self._target = test_word
        

    # Creates a GuessResult object with the user's guess and how it did against
    # the target word. This method is responsible for setting the values
    # in the returned object. The current word should not be stored
    # in the object unless the user has lost the game with this guess.
    def submit_guess_and_get_result(self, guess:str) -> GuessResult:
        # increment guesses and create GuessResult object
        self._turns_remain -= 1
        result = GuessResult(guess, self._turns_remain)

        # figure out GuessState
        # check if the word isn't the right length
        if (len(result.user_guess) != self._word_list._word_length or result.user_guess not in self._word_list._active_words):
            result.state = GuessState.INVALID_WORD
            self._turns_remain += 1
        else:
            # check if the valid word matches the target word
            if (result.user_guess == self._target):
                result.state = GuessState.YOU_WON
                self.has_won = True
            # check if the user has more guesses
            elif (self.has_more_guesses() == False):
                result.state = GuessState.YOU_LOST
                result.current_word = self._target
            # since the user guessed a valid word that isn't the target 
            # word and has more guesses, they get to gues again
            else:
                result.state = GuessState.GUESS_AGAIN
    
        # figure out letter states if word is valid
        if result.state != GuessState.INVALID_WORD:
        
            letter_state_list:List[LetterState] = []
            remaining_letters:List[str] = []

            # create a list of letter states to have proper indexes to work with
            for x in range (len(result.user_guess)): 
                letter_state_list.append(LetterState.NOT_FOUND)

            # first get any green letter matches
            for x in range(len(result.user_guess)):
                if result.user_guess[x] == self._target[x]:
                        letter_state_list[x] = LetterState.MATCH_PLACE
                else:
                    # take the remaining letters of the target word and put them in a list
                    remaining_letters.append(self._target[x])
            
            for x in range(len(remaining_letters)):
                for y in range(len(result.user_guess)):
                    # check if a letter matches the guess letter in any place
                    if (remaining_letters[x] == result.user_guess[y] and letter_state_list[y] == LetterState.NOT_FOUND):
                        letter_state_list[y] = LetterState.MATCH_LETTER
                        break
            result.letter_state = letter_state_list
                    

        return result