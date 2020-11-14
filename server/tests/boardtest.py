import unittest

import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from server.gamestate import GameState
from server.piece import Piece
from server.pawn import Pawn
from server.rook import Rook
from server.knight import Knight
from server.bishop import Bishop
from server.queen import Queen
from server.king import King


class BoardTest(unittest.TestCase):


    def test_board_build(self):
        state = GameState()

        actual = len(state.board)
        expected = 8

        self.assertEqual(actual, expected)

        count = 0

        for row in state.board:
            count += len(row)
        
        actual = count
        expected = 64

        self.assertEqual(actual, expected)


    def test_board_init_pieces(self):
        state = GameState()

        state.init_pieces()

        limit = 8

        for i in range(0, limit):
            for j in range(2, 6):
                self.assertIsNone(state.board[i][j])

        for i in range(0, limit):
            for j in range(0, 2):
                self.assertIsNotNone(state.board[i][j])

        for i in range(6, limit):
            for j in range(6, limit):
                self.assertIsNotNone(state.board[i][j])

        y = 1

        for i in range(0, limit):
            piece = state.board[i][y]
            self.assertIsInstance(state.board[i][y], Pawn)
            self.assertEqual(piece.color, Piece.black)

        y = 6

        for i in range(0, limit):
            piece = state.board[i][y]
            self.assertIsInstance(state.board[i][y], Pawn)
            self.assertEqual(piece.color, Piece.white)

        black_rooks = {state.board[0][0], state.board[7][0]}
        white_rooks = {state.board[0][7], state.board[7][7]}

        black_knights = {state.board[1][0], state.board[6][0]}
        white_knights = {state.board[1][7], state.board[6][7]}

        black_bishops = {state.board[2][0], state.board[5][0]}
        white_bishops = {state.board[2][7], state.board[5][7]}

        black_queen = state.board[3][0]
        white_queen = state.board[3][7]

        black_king = state.board[4][0]
        white_king = state.board[4][7]

        for piece in black_rooks:
            self.assertIsInstance(piece, Rook)
            self.assertEqual(piece.color, Piece.black)

        for piece in white_rooks:
            self.assertIsInstance(piece, Rook)
            self.assertEqual(piece.color, Piece.white)


        for piece in black_knights:
            self.assertIsInstance(piece, Knight)
            self.assertEqual(piece.color, Piece.black)

        for piece in white_knights:
            self.assertIsInstance(piece, Knight)
            self.assertEqual(piece.color, Piece.white)


        for piece in black_bishops:
            self.assertIsInstance(piece, Bishop)
            self.assertEqual(piece.color, Piece.black)

        for piece in white_bishops:
            self.assertIsInstance(piece, Bishop)
            self.assertEqual(piece.color, Piece.white)
    

    def test_is_checked(self):
        pass


    def test_parse_board(self):
        state = GameState()

        pawn = Pawn(3, 6, Piece.white, state)
        queen = Queen(7, 7, Piece.black, state)

        actual = state.parse_board()

        expected = list()

        for i in range(0, GameState.size):
            expected.append(list())
            for j in range(0, GameState.size):
                expected[i].append(None)

        expected[3][6] = {'cord' : (3, 6), 'type' : 'pawn', 'color' : Piece.white}
        expected[7][7] = {'cord' : (7, 7), 'type' : 'queen', 'color' : Piece.black}
    
        self.assertListEqual(actual, expected)


    def test_board_to_json(self):
        state = GameState()

        pawn = Pawn(3, 6, Piece.white, state)
        queen = Queen(7, 7, Piece.black, state)

        actual = state.state_to_json()
        expected = [
                    {'cord' : (3, 6), 'type' : 'pawn', 'color' : Piece.white},
                    {'cord' : (7, 7), 'type' : 'queen', 'color' : Piece.black}
                   ]
    
        self.assertListEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()

