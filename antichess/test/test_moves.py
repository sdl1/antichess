import unittest
from antichess.Board import Board
from antichess import Pieces
from antichess.Rules import Suicide

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

    def testBasicMoves(self):
        # TODO large scale move generation
        # Basic pawn move
        self.board.clear()
        self.board.setPiece("d2", Pieces.Pawn(0));
        validMoves = ["d2d3", "d2d4"];
        self.assertValidMoves(self.board, validMoves, 0)

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
        self.assertValidMoves(self.board, validMoves, 1, enforceCaptures=False)

if __name__=="__main__":
    unittest.main()
