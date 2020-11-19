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

        source_pre_json = piece.piece_to_json()

        move = state.make_move(source, target)

        self.assertIsNone(state.board[x][y])

        actual = state.board[x][y - 1]
        expected = piece

        self.assertEqual(actual, expected)

        actual = move
        expected = {
            'source' : source,
            'target' : target,
            'hit' : False,
            'log' : {
                'source_pre' : source_pre_json,
                'target_pre' : None
            }
        }

        self.assertDictEqual(actual, expected)


    def test_make_move_hit(self):
        state = GameState()

        x, y = 3, 6
        piece = Pawn(x, y, Piece.white, state)
        target_piece = Pawn(x - 1, y - 1, Piece.black, state)

        piece_pre_json = piece.piece_to_json()
        target_pre_json = target_piece.piece_to_json()

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
            'hit' : True,
            'log' : {
                'source_pre' : piece_pre_json,
                'target_pre' : target_pre_json
            }
        }

        self.assertDictEqual(actual, expected)



if __name__ == '__main__':
    unittest.main()
