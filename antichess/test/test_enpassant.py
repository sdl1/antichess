import unittest
from antichess.Board import Board
from antichess import Pieces
from antichess.Rules import Suicide
from antichess.Move import Move

class EnPassantTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.rules = Suicide()

    def assertValidMoves(self, board, moves, colour, enforceCaptures=True):
        self.board.displayAsText()
        v, _ = self.rules.getAllValidMoves(self.board, colour, enforceCaptures)
        v_str = map(str, v)
        moves_str = map(str, moves)
        print "Generated: ", v_str
        print "Asserted: ", moves_str
        self.assertTrue(set(v_str)==set(moves_str))

    def testEnPassantBasic(self):
        self.board.clear()
        # Before en passant
        self.board.setPiece("a5", Pieces.Pawn(0))
        self.board.setPiece("b7", Pieces.Pawn(1))
        self.board.setPiece("h3", Pieces.Pawn(0))
        self.assertValidMoves(self.board, ["a5a6", "h3h4"], 0)
        # En passant opportunity
        self.board.makeMove(Move.fromNotation("b7b5", 1))
        self.assertValidMoves(self.board, ["a5a6", "a5b6", "h3h4"], 0)
        # Opportunity passed
        self.board.makeMove(Move.fromNotation("h3h4", 0))
        self.assertValidMoves(self.board, ["a5a6", "h4h5"], 0)

    def testEnPassantUndo(self):
        self.board.clear()
        # Before en passant
        self.board.setPiece("a5", Pieces.Pawn(0))
        self.board.setPiece("b7", Pieces.Pawn(1))
        self.board.setPiece("h3", Pieces.Pawn(0))
        self.assertValidMoves(self.board, ["a5a6", "h3h4"], 0)
        # En passant opportunity
        self.board.makeMove(Move.fromNotation("b7b5", 1))
        self.assertValidMoves(self.board, ["a5a6", "a5b6", "h3h4"], 0)
        # Opportunity passed
        self.board.makeMove(Move.fromNotation("h3h4", 0))
        self.assertValidMoves(self.board, ["a5a6", "h4h5"], 0)
        # Undo h3h4
        self.board.retractMove()
        # Opportunity re-appears
        self.assertValidMoves(self.board, ["a5a6", "a5b6", "h3h4"], 0)

if __name__=="__main__":
    unittest.main()
