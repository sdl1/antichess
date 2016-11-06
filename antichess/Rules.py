import Board
import Pieces
import Move

class RulesViolation(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Suicide():
	def validate(self, move, board, col, enforceCaptures=True):
		# Allow null moves (passes)
		if move==Move.PASS:
			return True
		# Allow resignation
		if move==Move.RESIGN:
			return True
		# Allow retracting moves
		if move==Move.RETRACT:
			if len(board.movesMade)==0:
				raise RulesViolation("No moves to retract")
			print "Retracting move"
			return True

                # Basic validation - check it's within the board
                if move[0][0]<0 or move[0][0]>7 or move[0][1]<0 or move[0][1]>7:
                        raise RulesViolation("Invalid from square.")
                if move[1][0]<0 or move[1][0]>7 or move[1][1]<0 or move[1][1]>7:
                        raise RulesViolation("Invalid to square.")

		fr, to = move.unpack()

		# Can't move an empty square or other colour piece
		if board.pieces[fr] == None:
			raise RulesViolation("Tried to move empty square")
		if not board.pieces[fr].colour == col:
			raise RulesViolation("Tried to move opponent's piece")
		# Can't move onto own piece
		if not board.pieces[to] == None:
			if board.pieces[to].colour == col:
				raise RulesViolation("Tried to move onto own piece")
		# If not a knight, must have clear route
		frl = [fr/8, fr%8]
		tol = [to/8, to%8]
		if not isinstance(board.pieces[fr], Pieces.Knight) and not board.hasClearPath(frl, tol):
			raise RulesViolation("No clear path between to and from squares")

		# Check particular piece movement
		if not board.pieces[fr].canMakeMove(board, move):
			raise RulesViolation("Piece can't move like that")

		# Must make captures if possible
		if enforceCaptures:
                    if board.hasCaptures(col) and (board.pieces[to] == None) and (not move.isEnpassant(board)):
				raise RulesViolation("Captures are available")

		return True

	def getValidMoves(self, board, piece, colour, enforceCaptures=True):
		moves = []
		fr = piece
                # First, we get a (strictly optimistic) list of plausible places this piece could move to,
                # ignoring line of sight and promotions.
                # This is faster than checking validity of all possible moves.
                destList = board.pieces[fr[0]*8+fr[1]].getPlausibleMoves(fr)
                for to in destList:
			m = Move.Move(fr, to)
			try:
				self.validate( m, board, colour, enforceCaptures )
				moves.append( m )
			except RulesViolation as e:
				pass
                # Now consider promotion moves
		promotionPieces = [Pieces.Queen(colour), Pieces.Rook(colour), Pieces.Knight(colour), Pieces.Bishop(colour), Pieces.King(colour)]
                if isinstance(board.pieces[fr[0]*8+fr[1]], Pieces.Pawn):
                        row = fr[0]
                        if colour==0 and row==1:
                                for col in [fr[1]-1, fr[1], fr[1]+1]:
                                        to = [0, col]
                                        for pp in promotionPieces:
				                m = Move.PromotionMove(fr, to, pp)
				                try:
				                	self.validate( m, board, colour, enforceCaptures )
				                	moves.append( m )
				                except RulesViolation as e:
				                	pass
                        elif colour==1 and row==6:
                                for col in [fr[1]-1, fr[1], fr[1]+1]:
                                        to = [7, col]
                                        for pp in promotionPieces:
				                m = Move.PromotionMove(fr, to, pp)
				                try:
				                	self.validate( m, board, colour, enforceCaptures )
				                	moves.append( m )
				                except RulesViolation as e:
				                	pass
		return moves

	def getAllValidMoves(self, board, colour, enforceCaptures=True):
		validMoves = []
		isCapture = []
		# All my pieces
		pieces = board.getAllPieces(colour)
		for p in pieces:
			for m in self.getValidMoves(board, p, colour, enforceCaptures):
				validMoves.append(m)
				fr,to = m.unpack()
				capture = (not board.pieces[to] == None) or m.isEnpassant(board)
				isCapture.append(capture)

		return validMoves, isCapture





