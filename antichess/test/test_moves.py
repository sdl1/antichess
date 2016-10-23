import unittest
from antichess.Board import Board
from antichess import Pieces
from antichess.Rules import Suicide

# TODO large scale move generation

class MovesGenerationTest(unittest.TestCase):

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

    def testPawnMoves(self):
        self.board.clear()
        self.board.setPiece("d2", Pieces.Pawn(0));
        validMoves = ["d2d3", "d2d4"];
        self.assertValidMoves(self.board, validMoves, 0)
        self.board.clear()
        self.board.setPiece("a2", Pieces.Pawn(0));
        self.board.setPiece("h3", Pieces.Rook(1));
        validMoves = ["a2a3", "a2a4"];
        self.assertValidMoves(self.board, validMoves, 0)
        self.board.setPiece("h1", Pieces.Rook(0));
        validMoves = ["h1h3"]
        self.assertValidMoves(self.board, validMoves, 0)

    def testPrinting(self):
        # Test move generation in non-trivial board
        # The print statement catches some bugs due
        # to out of bounds indices
        self.board.clear()
        self.board.setPiece("a1", Pieces.Rook(0));
        self.board.setPiece("a2", Pieces.Pawn(0));
        self.board.setPiece("g1", Pieces.Knight(0));
        self.board.setPiece("h1", Pieces.Rook(0));
        self.board.setPiece("e2", Pieces.Pawn(0));
        self.board.setPiece("f2", Pieces.King(0));
        self.board.setPiece("h3", Pieces.Pawn(0));

        self.board.setPiece("a3", Pieces.Pawn(1));
        self.board.setPiece("g6", Pieces.Pawn(1));
        self.board.setPiece("a7", Pieces.Pawn(1));
        self.board.setPiece("e7", Pieces.Pawn(1));
        self.board.setPiece("f7", Pieces.Pawn(1));
        self.board.setPiece("h7", Pieces.Pawn(1));
        self.board.setPiece("d7", Pieces.King(1));
        self.board.setPiece("h8", Pieces.Rook(1));
        self.board.displayAsText()
        v, _ = self.rules.getAllValidMoves(self.board, 0, enforceCaptures=True)
        for move in v:
            print move
        self.assertTrue(len(v)>1)

    def testPromotionMoves(self):
        # Promotion moves
        self.board.clear()
        self.board.setPiece("c7", Pieces.Pawn(0));
        self.board.setPiece("d8", Pieces.Knight(1));
        self.board.setPiece("f7", Pieces.Pawn(0));
        self.board.setPiece("a2", Pieces.Pawn(1));
        self.board.setPiece("b1", Pieces.Knight(0));
        self.board.setPiece("f2", Pieces.Pawn(1));
        # Without enforcing captures
        validMoves = ["c7c8R", "c7c8N", "c7c8B", "c7c8Q", "c7c8K", \
                      "c7d8R", "c7d8N", "c7d8B", "c7d8Q", "c7d8K", \
                      "f7f8R", "f7f8N", "f7f8B", "f7f8Q", "f7f8K", \
                      "b1a3", "b1c3", "b1d2"]
        self.assertValidMoves(self.board, validMoves, 0, enforceCaptures=False)
        validMoves = ["a2a1R", "a2a1N", "a2a1B", "a2a1Q", "a2a1K", \
                      "a2b1R", "a2b1N", "a2b1B", "a2b1Q", "a2b1K", \
                      "f2f1R", "f2f1N", "f2f1B", "f2f1Q", "f2f1K", \
                      "d8b7", "d8c6", "d8e6", "d8f7"]
        self.assertValidMoves(self.board, validMoves, 1, enforceCaptures=False)
        # With enforcing captures
        validMoves = ["c7d8R", "c7d8N", "c7d8B", "c7d8Q", "c7d8K"]
        self.assertValidMoves(self.board, validMoves, 0)
        validMoves = ["a2b1R", "a2b1N", "a2b1B", "a2b1Q", "a2b1K", \
                      "d8f7"]
        self.assertValidMoves(self.board, validMoves, 1)

    def testRookMoves(self):
        self.board.clear()
        self.board.setPiece("c2", Pieces.Rook(0))
        validMoves = ["c2a2", "c2b2", "c2d2", "c2e2", "c2f2", "c2g2", "c2h2", \
                "c2c1", "c2c3", "c2c4", "c2c5", "c2c6", "c2c7", "c2c8"]
        self.assertValidMoves(self.board, validMoves, 0)
        self.board.clear()
        self.board.setPiece("c2", Pieces.Rook(1))
        self.assertValidMoves(self.board, validMoves, 1)

    def testKnightMoves(self):
        self.board.clear()
        self.board.setPiece("d4", Pieces.Knight(0))
        validMoves = ["d4c2", "d4e2", "d4b3", "d4b5", "d4c6", "d4e6", "d4f5", "d4f3"]
        self.assertValidMoves(self.board, validMoves, 0)
        self.board.clear()
        self.board.setPiece("d4", Pieces.Knight(1))
        self.assertValidMoves(self.board, validMoves, 1)

    def testBishopMoves(self):
        self.board.clear()
        self.board.setPiece("f3", Pieces.Bishop(0))
        validMoves = ["f3d1", "f3e2", "f3g4", "f3h5", "f3g2", "f3h1", "f3e4", "f3d5", "f3c6", "f3b7", "f3a8"]
        self.assertValidMoves(self.board, validMoves, 0)
        self.board.clear()
        self.board.setPiece("f3", Pieces.Bishop(1))
        self.assertValidMoves(self.board, validMoves, 1)

    def testKingMoves(self):
        self.board.clear()
        self.board.setPiece("a1", Pieces.King(0))
        self.board.setPiece("e5", Pieces.King(0))
        validMoves = ["a1a2", "a1b2", "a1b1", \
                      "e5e4", "e5e6", "e5d5", "e5f5", "e5d4", "e5f6", "e5f4", "e5d6"]
        self.assertValidMoves(self.board, validMoves, 0)
        self.board.clear()
        self.board.setPiece("a1", Pieces.King(1))
        self.board.setPiece("e5", Pieces.King(1))
        self.assertValidMoves(self.board, validMoves, 1)

if __name__=="__main__":
    unittest.main()
