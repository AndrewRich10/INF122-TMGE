from Bejeweled import *
import unittest

class Test_Bejeweled(unittest.TestCase):
    def test_board_initializes_unmatching_and_future_matching(self):
        for i in range(0, 1000):
            game = Bejeweled([PlayerProfile(1, [], 0, 0)])
            assert(not game._matchesExist(game._board))
            assert(game._futureMatchesExist(game._board))
            


if __name__ == '__main__':
    unittest.main()