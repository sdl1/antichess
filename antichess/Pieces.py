import Move

import sys
class bcolours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[92m'
    YELLOW = '\033[33m'
    BLUE = '\033[94m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'


    ENDC = '\033[0m'

    #PIECECOLOUR = [OKGREEN, OKBLUE]
    #PIECECOLOURALT = [WARNING, FAIL]
    PIECECOLOUR = [GREEN, BLUE]
    PIECECOLOURALT = [WHITE, CYAN]

class Piece:
	colour = None
	symbol = None
	altsymbol = None
	def __init__(self, col, sym, alt=u'\u2656'):
		self.colour = col
		self.symbol = sym
		self.altsymbol = alt
	def displayAsText(self, alt=False):
		if alt:
			print bcolours.PIECECOLOURALT[self.colour] + self.symbol + bcolours.ENDC,
			#print bcolours.PIECECOLOUR[self.colour] + self.altsymbol + bcolours.ENDC,
		else:
			print bcolours.PIECECOLOUR[self.colour] + self.symbol + bcolours.ENDC,


#NOTE: canMakeMove ignores whether or not there are pieces in the way

class Pawn(Piece):
	def __init__(self, col):
		Piece.__init__(self, col, "p", u'\u2659')

        def getPlausibleMoves(self, fr):
                # Ignoring promotion but including double move
                row, col = fr[0], fr[1]
                if self.colour==0:
                            torow = fr[0]-1
                            moves = [ [torow, col-1], [torow, col], [torow, col+1], [row-2, col] ]
                else:
                            torow = fr[0]+1
                            moves = [ [torow, col-1], [torow, col], [torow, col+1], [row+2, col] ]
                return moves

	def canMakeMove(self, board, move):
		fr, to = move[0], move[1]
		# White
		if self.colour==0:
			# First check for captures:
			if abs(to[1]-fr[1])==1 and to[0]==fr[0]-1:
				if fr[0]==1:
				        # Promotion with capture
					return board.hasPieceOn(to[0], to[1]) and board.getPieceOn(to).colour==1 and isinstance(move, Move.PromotionMove)
				else:
					return board.hasPieceOn(to[0], to[1]) and board.getPieceOn(to).colour==1
			# No capture -> can't move sideways
			if not to[1]==fr[1]:
				return False
			# Can't move onto a piece
			if board.hasPieceOn(to[0], to[1]):
				return False
			# First move can be double
			if fr[0]==6:
				return (to[0]==5 or to[0]==4) 
			# Promotion (no capture, that was checked above)
			if fr[0]==1:
				return to[0]==fr[0]-1 and isinstance(move, Move.PromotionMove)
			# Standard
			return to[0]==fr[0]-1
		# Black
		else:
			# First check for captures:
			if abs(to[1]-fr[1])==1 and to[0]==fr[0]+1:
				if fr[0]==6:
				        # Promotion with capture
					return board.hasPieceOn(to[0], to[1]) and board.getPieceOn(to).colour==0 and isinstance(move, Move.PromotionMove)
                                else:
				        return board.hasPieceOn(to[0], to[1]) and board.getPieceOn(to).colour==0
			# Can't move onto a piece
			if board.hasPieceOn(to[0], to[1]):
				return False
			# Can't move sideways
			if not to[1]==fr[1]:
				return False
			# First move can be double
			if fr[0]==1:
				return (to[0]==2 or to[0]==3) 
			# Promotion (no capture, that was checked above)
			if fr[0]==6:
				return to[0]==fr[0]+1 and isinstance(move, Move.PromotionMove)
			# Standard
			return to[0]==fr[0]+1
		return False


class King(Piece):
	def __init__(self, col):
		Piece.__init__(self, col, "K", u'\u2654')
        def getPlausibleMoves(self, fr):
                moves = []
                for row in [fr[0]-1, fr[0], fr[0]+1]:
                        for col in [fr[1]-1, fr[1], fr[1]+1]:
                                if not (row==fr[0] and col==fr[1]): moves.append([row,col])
                return moves

	def canMakeMove(self, board, move):
		fr, to = move[0], move[1]
		return ( abs(fr[0]-to[0]) <= 1 and abs(fr[1]-to[1]) <= 1 )

class Queen(Piece):
	def __init__(self, col):
		Piece.__init__(self, col, "Q", u'\u2655')
        def getPlausibleMoves(self, fr):
                movesRook = Rook(self.colour).getPlausibleMoves(fr)
                movesBishop = Bishop(self.colour).getPlausibleMoves(fr)
                return movesRook + movesBishop
	def canMakeMove(self, board, move):
		fr, to = move[0], move[1]
		if (fr[1]==to[1] or fr[0]==to[0]):
			return True
		elif ( abs(fr[0]-to[0]) == abs(fr[1]-to[1]) ):
			return True
		else:
			return False

class Rook(Piece):
	def __init__(self, col):
		Piece.__init__(self, col, "R", u'\u2656')
        def getPlausibleMoves(self, fr):
                moves = []
                for col in range(0,7):
                    moves.append([fr[0], col])
                for row in range(0,7):
                    moves.append([row, col])
                return moves
	def canMakeMove(self,board, move):
		fr, to = move[0], move[1]
		return (fr[1]==to[1] or fr[0]==to[0])

class Knight(Piece):
	def __init__(self, col):
		Piece.__init__(self, col, "N", u'\u2658')
        def getPlausibleMoves(self, fr):
                moves = []
                r,c = fr[0], fr[1]
                # Left
                if c>1:
                    if r>0:
                        moves.append([r-1,c-2])
                    if r<7:
                        moves.append([r+1,c-2])
                # Right
                if c<6:
                    if r>0:
                        moves.append([r-1,c+2])
                    if r<7:
                        moves.append([r+1,c+2])
                # Up
                if r>1:
                    if c>0:
                        moves.append([r-2,c-1])
                    if c<7:
                        moves.append([r-2,c+1])
                # Down
                if r<6:
                    if c>0:
                        moves.append([r+2,c-1])
                    if c<7:
                        moves.append([r+2,c+1])
                return moves
	def canMakeMove(self,board, move):
		fr, to = move[0], move[1]
		return ( abs(fr[0]-to[0])==2 and abs(fr[1]-to[1])==1 ) or ( abs(fr[1]-to[1])==2 and abs(fr[0]-to[0])==1 )

class Bishop(Piece):
	def __init__(self, col):
		Piece.__init__(self, col, "B", u'\u2657')
        def getPlausibleMoves(self, fr):
                moves = []
                r,c = fr[0], fr[1]
                while r<7 and c<7:
                    r = r+1
                    c = c+1
                    moves.append([r,c])
                r,c = fr[0], fr[1]
                while r>=1 and c>=1:
                    r = r-1
                    c = c-1
                    moves.append([r,c])
                r,c = fr[0], fr[1]
                while r>=1 and c<7:
                    r = r-1
                    c = c+1
                    moves.append([r,c])
                while r<7 and c>=1:
                    r = r+1
                    c = c-1
                    moves.append([r,c])
                return moves
	def canMakeMove(self,board, move):
		fr, to = move[0], move[1]
		return ( abs(fr[0]-to[0]) == abs(fr[1]-to[1]) )


