import unittest

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from server.gamestate import GameState
from server.piece import Piece
from server.pawn import Pawn
from server.rook import Rook
from server.knight import Knight
from server.bishop import Bishop
from server.queen import Queen
from server.king import King

class PieceTest(unittest.TestCase):


    def test_pawn_movable(self):
        state = GameState()

        """
            O
            P
        """

        x, y = 3, 6
        pawn = Pawn(x, y, Piece.white, state)
        pawn.idle = False
        actual = set(pawn.get_movable())
        expected = {(3, 5)}
        self.assertSetEqual(actual, expected)

        pawn.color = Piece.black
        actual = set(pawn.get_movable())
        expected = {(3, 7)}
        self.assertSetEqual(actual, expected)
        

        """
            +-
            |P
        """

        x, y = 0, 0
        pawn = Pawn(x, y, Piece.white, state)
        pawn.idle = False
        actual = set(pawn.get_movable())
        expected = set()
        self.assertSetEqual(actual, expected)

        pawn.color = Piece.black
        actual = set(pawn.get_movable())
        expected = {(0, 1)}
        self.assertSetEqual(actual, expected)

        """
            -+
            B|
            P|
        """

        x, y = 7, 1
        block_x, block_y = 7, 0
        pawn = Pawn(x, y, Piece.white, state)
        pawn.idle = False
        blocker = Pawn(block_x, block_y, Piece.black, state)
        actual = set(pawn.get_movable())
        expected = set()
        self.assertSetEqual(actual, expected)


    def test_pawn_idle_movable(self):
        state = GameState()
        
        """
            O
            O       
            P
        """
        x, y = 3, 6
        pawn = Pawn(x, y, Piece.white, state)
        actual = set(pawn.get_movable())
        expected = {(3, 5), (3, 4)}
        self.assertSetEqual(actual, expected)

        
        pawn.color = Piece.black
        actual = set(pawn.get_movable())
        expected = {(3, 7)}
        self.assertSetEqual(actual, expected)

        pawn.color = Piece.white
        
        """
            B
            O
            P
        """
        block_x, block_y = 3, 4
        blocker_a = Pawn(block_x, block_y, Piece.white, state)
        actual = set(pawn.get_movable())
        expected = {(3, 5)}
        self.assertSetEqual(actual, expected)

        """
            B
            B
            P
        """
        block_x, block_y = 3, 5
        blocker_b = Pawn(block_x, block_y, Piece.white, state)
        actual = set(pawn.get_movable())
        expected = set()
        self.assertSetEqual(actual, expected)
        
        """
            B
            P
        """
        state.board[3][4] = None
        expected = set(pawn.get_movable())
        actual = set()
        self.assertSetEqual(actual, expected)

        """
            +-
            |O
            |P
        """
        x, y = 0, 1
        pawn = Pawn(x, y, Piece.white, state)
        actual = set(pawn.get_movable())
        expected = {(0, 0)}
        self.assertSetEqual(actual, expected)

        """
            -+
            P|
        """
        x, y = 7, 0
        pawn = Pawn(x, y, Piece.white, state)
        actual = set(pawn.get_movable())
        expected = set()

        self.assertSetEqual(actual, expected)


    def test_pawn_target_movable(self):
        state = GameState()

        """
            O
            OT
            P
        """
        pa_x, pa_y = 3, 6
        ta_x, ta_y = 4, 5
        pawn_a = Pawn(pa_x, pa_y, Piece.white, state)
        target_a = Pawn(ta_x, ta_y, Piece.black, state)
        actual = set(pawn_a.get_movable())
        expected = {(3, 5), (4, 5), (3, 4)}
        self.assertSetEqual(actual, expected)

        """
            OT
            P
        """
        pawn_a.idle = False
        actual = set(pawn_a.get_movable())
        expected = {(3, 5), (4, 5)}
        self.assertSetEqual(actual, expected)

        """
            --+
            TO|
             P|
        """
        pb_x, pb_y = 7, 1
        tb_x, tb_y = 6, 0
        pawn_b = Pawn(pb_x, pb_y, Piece.white, state)
        target_b = Pawn(tb_x, tb_y, Piece.black, state)
        actual = set(pawn_b.get_movable())
        expected = {(6, 0), (7, 0)}
        self.assertSetEqual(actual, expected)


    def test_rook_movable(self):
        state = GameState()

        x, y = 3, 6
        rook = Rook(x, y, Piece.white, state)

        actual = set(rook.get_movable())
        expected = {(4, 6), (5, 6), (6, 6), (7, 6),
                    (2, 6), (1, 6), (0, 6),
                    (3, 7),
                    (3, 5), (3, 4), (3, 3), (3, 2), (3, 1), (3, 0)}

        self.assertSetEqual(actual, expected)

        blocker_a = Pawn(3, 7, Piece.white, state)
        blocker_b = Pawn(1, 6, Piece.white, state)

        actual = set(rook.get_movable())
        expected = {(4, 6), (5, 6), (6, 6), (7, 6),
                    (2, 6),
                    (3, 5), (3, 4), (3, 3), (3, 2), (3, 1), (3, 0)}

        self.assertSetEqual(actual, expected)


    def test_rook_target_movable(self):
        state = GameState()

        x, y = 3, 6
        rook = Rook(x, y, Piece.white, state)
        
        target_a = Pawn(3, 3, Piece.black, state)
        target_b = Pawn(4, 6, Piece.black, state)

        actual = set(rook.get_movable())
        expected = {(4, 6),
                    (2, 6), (1, 6), (0, 6),
                    (3, 7),
                    (3, 5), (3, 4), (3, 3)}

        self.assertSetEqual(actual, expected)


    def test_knight_movable(self):
        state = GameState()

        x, y = 3, 6
        knight = Knight(x, y, Piece.white, state)

        actual = set(knight.get_movable())
        expected = {(4, 4), (5, 5), (5, 7), (1, 7), (1, 5), (2, 4)}

        self.assertSetEqual(actual, expected)

        blocker_a = Pawn(5, 5, Piece.white, state)
        blocker_b = Pawn(2, 4, Piece.white, state)

        actual = set(knight.get_movable())
        expected = {(4, 4), (5, 7), (1, 7), (1, 5)}

        self.assertSetEqual(actual, expected)


    def test_knight_target_movable(self):
        state = GameState()

        x, y = 3, 6
        knight = Knight(x, y, Piece.white, state)

        target = Pawn(4, 4, Piece.black, state)

        actual = set(knight.get_movable())
        expected = {(4, 4), (5, 5), (5, 7), (1, 7), (1, 5), (2, 4)}

        self.assertSetEqual(actual, expected)
    

    def test_bishop_movable(self):
        state = GameState()

        x, y = 3, 6

        bishop = Bishop(x, y, Piece.white, state)

        actual = set(bishop.get_movable())
        expected = {(4, 5), (5, 4), (6, 3), (7, 2),
                    (4, 7),
                    (2, 7),
                    (2, 5), (1, 4), (0, 3)}

        self.assertSetEqual(actual, expected)


        blocker_a = Pawn(6, 3, Piece.white, state)
        blocker_b = Pawn(2, 5, Piece.white, state)

        actual = set(bishop.get_movable())
        expected = {(4, 5), (5, 4),
                    (4, 7),
                    (2, 7)}

        self.assertSetEqual(actual, expected)


    def test_bishop_target_movable(self):
        state = GameState()

        x, y = 3, 6

        bishop = Bishop(x, y, Piece.white, state)

        target_a = Pawn(5, 4, Piece.black, state)
        target_b = Pawn(2, 7, Piece.black, state)

        actual = set(bishop.get_movable())
        expected = {(4, 5), (5, 4),
                    (4, 7),
                    (2, 7),
                    (2, 5), (1, 4), (0, 3)}

        self.assertSetEqual(actual, expected)
    

    def test_queen_movable(self):
        state = GameState()

        x, y = 3, 6

        queen = Queen(x, y, Piece.white, state)

        actual = set(queen.get_movable())
        expected = {(3, 5), (3, 4), (3, 3), (3, 2), (3, 1), (3, 0),
                    (4, 5), (5, 4), (6, 3), (7, 2),
                    (4, 6), (5, 6), (6, 6), (7, 6),
                    (4, 7),
                    (3, 7),
                    (2, 7),
                    (2, 6), (1, 6), (0, 6),
                    (2, 5), (1, 4), (0, 3)}

        self.assertSetEqual(actual, expected)

        blocker_a = Pawn(3, 0, Piece.white, state)
        blocker_b = Pawn(4, 5, Piece.white, state)
        blocker_b = Pawn(6, 6, Piece.white, state)
        blocker_d = Pawn(2, 7, Piece.white, state)

        actual = set(queen.get_movable())
        expected = {(3, 5), (3, 4), (3, 3), (3, 2), (3, 1),
                    (4, 6), (5, 6),
                    (4, 7),
                    (3, 7),
                    (2, 6), (1, 6), (0, 6),
                    (2, 5), (1, 4), (0, 3)}

        self.assertSetEqual(actual, expected)


    def test_queen_target_movable(self):
        state = GameState()

        x, y = 3, 6

        queen = Queen(3, 6, Piece.white, state)

        target_a = Pawn(3, 5, Piece.black, state)
        target_b = Pawn(4, 7, Piece.black, state)
        target_c = Pawn(1, 6, Piece.black, state)

        actual = set(queen.get_movable())
        expected = {(3, 5),
                    (4, 5), (5, 4), (6, 3), (7, 2),
                    (4, 6), (5, 6), (6, 6), (7, 6),
                    (3, 7),
                    (4, 7),
                    (2, 7),
                    (2, 6), (1, 6),
                    (2, 5), (1, 4), (0, 3)}

        self.assertSetEqual(actual, expected)
        

    def test_king_movable(self):
        state = GameState()

        x, y = 3, 6
        king = King(x, y, Piece.white, state)

        actual = set(king.get_movable())
        expected = {(2, 5), (3, 5), (4, 5), (2, 6),
                    (4, 6), (2, 7), (3, 7), (4, 7)}
        
        self.assertSetEqual(actual, expected)

        x, y = 7, 0
        king = King(x, y, Piece.white, state)
        
        blocker = Pawn(6, 1, Piece.white, state)

        actual = set(king.get_movable())
        expected = {(6, 0), (7, 1)}

        self.assertSetEqual(actual, expected)


    def test_king_target_movable(self):
        state = GameState()

        x, y = 3, 6
        king = King(x, y, Piece.white, state)

        target = Pawn(3, 7, Piece.black, state)
        blocker = Pawn(4, 7, Piece.white, state)

        actual = set(king.get_movable())
        expected = {(2, 5), (3, 5), (4, 5), (2, 6),
                    (4, 6), (2, 7), (3, 7)}
        
        self.assertSetEqual(actual, expected)


    def test_check(self):
        state = GameState()

        x, y = 3, 6

        white_king = King(x, y, Piece.white, state)
        black_pawn = Pawn(x - 1, y - 1, Piece.black, state)

        actual = state.is_checked(state.board, 0)
        self.assertTrue(actual)
        
        actual = state.is_checked(state.board, 1)
        self.assertFalse(actual)


        state.board[x - 1][y - 1] = None

        black_pawn = Pawn(x - 1, y - 2, Piece.black, state)

        actual = state.is_checked(state.board, 0)
        self.assertFalse(actual)

        actual = state.is_checked(state.board, 1)
        self.assertFalse(actual)


        state.board[x - 1][y - 2] = None

        black_rook = Rook(x, y - 1, Piece.black, state)

        actual = state.is_checked(state.board, 0)
        self.assertTrue(actual)

        actual = set(white_king.get_movable())
        expected = {(3, 5),
                    (2, 6), (4, 6),
                    (2, 7), (4, 7)}

        self.assertSetEqual(actual, expected)


    def test_check_king_block(self):
        state = GameState()

        x, y = 3, 6

        white_king = King(x, y, Piece.white, state)
        black_pawn = Pawn(x, y - 2, Piece.black, state)

        black_pawn.idle = False

        actual = set(white_king.get_movable())
        expected = {(3, 5),
                    (2, 6), (4, 6),
                    (2, 7), (3, 7), (4, 7)}

        self.assertSetEqual(actual, expected)
        
        actual = state.is_checked(state.board, 0)
        self.assertFalse(actual)

        actual = state.is_checked(state.board, 1)
        self.assertFalse(actual)


    def test_check_move_block(self):
        state = GameState()

        x, y = 3, 6

        white_king = King(x, y, Piece.white, state)
        white_rook = Rook(x, y - 2, Piece.white, state)

        actual = set(white_king.get_movable())
        expected = {(2, 5), (3, 5), (4, 5),
                    (2, 6), (4, 6),
                    (2, 7), (3, 7), (4, 7)}

        self.assertSetEqual(actual, expected)

        actual = set(white_rook.get_movable())
        expected = {(3, 3), (3, 2), (3, 1), (3, 0), 
                    (4, 4), (5, 4), (6, 4), (7, 4),
                    (3, 5),
                    (2, 4), (1, 4), (0, 4)}

        self.assertSetEqual(actual, expected)

        actual = state.is_checked(state.board, 0)
        self.assertFalse(actual)
        

        black_rook = Rook(x, y - 4, Piece.black, state)

        actual = set(white_king.get_movable())
        expected = {(2, 5), (3, 5), (4, 5),
                    (2, 6), (4, 6),
                    (2, 7), (3, 7), (4, 7)}

        self.assertSetEqual(actual, expected) 

        actual = set(white_rook.get_movable())
        expected = {(3, 3), (3, 2),   
                    (3, 5)}

        self.assertSetEqual(actual, expected)

        actual = state.is_checked(state.board, 0)
        self.assertFalse(actual)


        black_queen = Queen(x - 1, y - 4, Piece.black, state)

        actual = set(white_king.get_movable())
        expected = {(3, 5), (4, 5),
                    (4, 6),
                    (3, 7), (4, 7)}

        self.assertSetEqual(actual, expected) 

        actual = set(white_rook.get_movable())
        expected = {(3, 3), (3, 2),   
                    (3, 5)}

        self.assertSetEqual(actual, expected)

        actual = state.is_checked(state.board, 0)
        self.assertFalse(actual)


if __name__ == '__main__':
    unittest.main()

