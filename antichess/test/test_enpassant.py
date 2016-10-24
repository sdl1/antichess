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

    def testEnPassantWhite(self):
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

    def testEnPassantBlack(self):
        self.board.clear()
        # Before en passant
        self.board.setPiece("a4", Pieces.Pawn(1))
        self.board.setPiece("b2", Pieces.Pawn(0))
        self.board.setPiece("h3", Pieces.Pawn(1))
        self.assertValidMoves(self.board, ["a4a3", "h3h2"], 1)
        # En passant opportunity
        self.board.makeMove(Move.fromNotation("b2b4", 0))
        self.assertValidMoves(self.board, ["a4a3", "a4b3", "h3h2"], 1)
        # Opportunity passed
        self.board.makeMove(Move.fromNotation("h3h2", 1))
        self.assertValidMoves(self.board, ["a4a3", "h3h2"], 1)

    def testEnPassantWhiteUndo(self):
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
        # Try lots of undos
        self.board.makeMove(Move.fromNotation("h3h4", 0))
        self.board.makeMove(Move.fromNotation("h4h5", 0))
        self.board.makeMove(Move.fromNotation("b5b4", 1))
        self.board.makeMove(Move.fromNotation("h5h6", 0))
        self.board.makeMove(Move.fromNotation("b4b3", 1))
        self.board.makeMove(Move.fromNotation("h7h8", 0))
        self.board.retractMove()
        self.board.retractMove()
        self.board.retractMove()
        self.board.retractMove()
        self.board.retractMove()
        # Not valid yet...
        self.assertValidMoves(self.board, ["a5a6", "h4h5"], 0)
        self.board.retractMove()
        # Now valid en passant
        self.assertValidMoves(self.board, ["a5a6", "a5b6", "h3h4"], 0)

if __name__=="__main__":
    unittest.main()
