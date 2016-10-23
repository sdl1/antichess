from .. import Rules
from .. import Board

# python -m antichess.test.perft

rules = Rules.Suicide()

def perft(board, depth, colour):
    nodes = 0
    if depth==0:
        return 1
    moves, _ = rules.getAllValidMoves(board, colour, enforceCaptures=False)
    for move in moves:
        board.makeMove(move)
        nodes = nodes + perft(board, depth-1, 1-colour)
        board.retractMove()
    return nodes

if __name__=="__main__":
    board = Board.Board()
    print perft(board, 3, 0)
