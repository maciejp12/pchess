import unittest

import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from server.gamestate import GameState
from server.piece import Piece
from server.pawn import Pawn

class ActionTest(unittest.TestCase):

    def test_make_move(self):
        state = GameState()

        x, y = 3, 6
        piece = Pawn(x, y, Piece.white, state)

        source = (x, y)
        target = (x, y - 1)

        move = state.make_move(source, target)

        self.assertIsNone(state.board[x][y])

        actual = state.board[x][y - 1]
        expected = piece

        self.assertEqual(actual, expected)

        actual = move
        expected = {
            'source' : source,
            'target' : target,
            'hit' : False
        }

        self.assertDictEqual(actual, expected)


    def test_make_move_hit(self):
        state = GameState()

        x, y = 3, 6
        piece = Pawn(x, y, Piece.white, state)
        target_piece = Pawn(x - 1, y - 1, Piece.black, state)

        source = (x, y)
        target = (x - 1, y - 1)

        move = state.make_move(source, target)

        self.assertIsNone(state.board[x][y])

        actual = state.board[x - 1][y - 1]
        expected = piece

        self.assertEqual(actual, expected)

        actual = move
        expected = {
            'source' : source,
            'target' : target,
            'hit' : True
        }

        self.assertDictEqual(actual, expected)



if __name__ == '__main__':
    unittest.main()
