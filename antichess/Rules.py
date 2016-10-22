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
		#TODO
		if not board.pieces[fr].canMakeMove(board, move):
			raise RulesViolation("Piece can't move like that")

		# Must make captures if possible
		if enforceCaptures:
			if board.hasCaptures(col) and board.pieces[to] == None:
				raise RulesViolation("Captures are available")

		return True

	def getValidMoves(self, board, piece, colour, enforceCaptures=True):
		moves = []
		fr = piece
		for row in range(0, 8):
			for col in range(0, 8):
				to = [row, col]
				#m = [ 8*fr[0] + fr[1], 8*to[0] + to[1] ]
				m = Move.Move(fr, to)
				try:
					self.validate( m, board, colour, enforceCaptures )
					#moves.append( [fr, to] )
					moves.append( m )
				except RulesViolation as e:
					pass
		return moves

	def getAllValidMoves(self, board, colour):
		validMoves = []
		isCapture = []
		# All my pieces
		pieces = board.getAllPieces(colour)
		for p in pieces:
			for m in self.getValidMoves(board, p, colour):
				validMoves.append(m)
				fr,to = m.unpack()
				isCapture.append( not board.pieces[ to ] == None )

		return validMoves, isCapture





