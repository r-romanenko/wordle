import unittest
from wordle import WordList


class WordListTestCases(unittest.TestCase):
    def setUp(self) -> None:
        self.word_list = WordList()
        return super().setUp()
        
    def test_word_length(self):
        self.word_list.set_active_word_length(5)
        self.assertEqual(self.word_list._word_length, 5)
        for word in self.word_list._active_words:
            self.assertEqual(5, len(word))

        self.word_list.set_active_word_length(6)
        self.assertEqual(self.word_list._word_length, 6)
        for word in self.word_list._active_words:
            self.assertEqual(6, len(word))

    def test_random_valid_word(self):
        self.word_list.set_active_word_length(5)
        test_word = self.word_list.pick_random_word()
        self.assertTrue(self.word_list.is_valid_word(test_word))
        self.assertFalse(self.word_list.is_valid_word("ZZZZZ"))
