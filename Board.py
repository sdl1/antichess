import Pieces
import Rules
import Move
import sys

class Board:
	pieces = []
	WHITE = 0
	BLACK = 1
	movesMade = []
	def __init__(self):
		self.pieces.append(Pieces.Rook(self.BLACK))
		self.pieces.append(Pieces.Knight(self.BLACK))
		self.pieces.append(Pieces.Bishop(self.BLACK))
		self.pieces.append(Pieces.Queen(self.BLACK))
		self.pieces.append(Pieces.King(self.BLACK))
		self.pieces.append(Pieces.Bishop(self.BLACK))
		self.pieces.append(Pieces.Knight(self.BLACK))
		self.pieces.append(Pieces.Rook(self.BLACK))

		for i in range(9,17):
			self.pieces.append(Pieces.Pawn(self.BLACK))

		for i in range(17, 65-16):
			self.pieces.append(None)

		for i in range(65-16,65-8):
			self.pieces.append(Pieces.Pawn(self.WHITE))

		self.pieces.append(Pieces.Rook(self.WHITE))
		self.pieces.append(Pieces.Knight(self.WHITE))
		self.pieces.append(Pieces.Bishop(self.WHITE))
		self.pieces.append(Pieces.Queen(self.WHITE))
		self.pieces.append(Pieces.King(self.WHITE))
		self.pieces.append(Pieces.Bishop(self.WHITE))
		self.pieces.append(Pieces.Knight(self.WHITE))
		self.pieces.append(Pieces.Rook(self.WHITE))

	def displayAsText(self):
		lastMove = self.getLastMove()
		print "--a-b-c-d-e-f-g-h--"
		for row in range(8):
			sys.stdout.write(str(9 - (row+1)))
			sys.stdout.write("|")
			for col in range(8):
				idx = 8*row + col
				p = self.pieces[idx]
				if (row==lastMove[0][0] and col==lastMove[0][1]) or (row==lastMove[1][0] and col==lastMove[1][1]):
					if p==None:
						sys.stdout.write(Pieces.bcolours.PIECECOLOURALT[ self.getLastMovedPiece().colour  ] +  "." + Pieces.bcolours.ENDC)
					else:
						p.displayAsText(alt=True)
				else:
					if p==None:
						sys.stdout.write(" ")
					else:
						p.displayAsText()
				sys.stdout.write("|")

		#	print "-----------------"
			print 9-(row+1)
		#print "-----------------"
		print "--a-b-c-d-e-f-g-h--"

	def makeMove(self, move):
		# Allow null moves (passes)
		if move==Move.PASS:
			return
		# Allow retracting move
		if move==Move.RETRACT:
			self.retractMove()
			return
		fr, to = move.unpack()
		self.movesMade.append( [move, self.pieces[to]] )

		self.pieces[ to ] = self.pieces[ fr ]
		self.pieces[ fr ] = None
		if isinstance(move, Move.PromotionMove):
			self.pieces[ to ] = move.promoteTo

	def retractMove(self):
		if len(self.movesMade)==0:
			return
		[move, piece] = self.movesMade.pop()
		fr, to = move.unpack()
		self.pieces[ fr ] = self.pieces[ to ]
		self.pieces[ to ] = piece
		if isinstance(move, Move.PromotionMove):
			self.pieces[ fr ] = Pieces.Pawn( self.pieces[fr].colour )

	def getLastMove(self):
		if len(self.movesMade)==0:
			return Move.NONE
		return self.movesMade[-1][0]
	
	def getLastMovedPiece(self):
		if len(self.movesMade)==0:
			return None
		fr, to = self.getLastMove().unpack()
		return self.pieces[to]

	def hasCaptures(self, colour):
		#TODO
		# All my pieces
		pieces = self.getAllPieces(colour)
		for p in pieces:
			for m in Rules.Suicide().getValidMoves(self, p, colour, False):
				to = m[1]
				if not self.pieces[ 8*to[0]+to[1] ]==None:
					return True
		return False

	def hasPieceOn(self, row, col):
		return not (self.pieces[row*8+col] == None)

	def getPieceOn(self, m):
		row = m[0]
		col = m[1]
		return self.pieces[row*8+col]

	def hasClearPath(self, fr, to):
		def sign(x):
			if x > 0:
				return 1
			if x < 0:
				return -1
			return 0
		# check for bishop move first
		if abs(fr[0]-to[0]) == abs(fr[1]-to[1]):
			if fr[1]>to[1]:
				fr, to = to, fr
			s = [sign(to[0] - fr[0]), sign(to[1]-fr[1])]
			for inc in range(1, to[1]-fr[1]):
				if self.hasPieceOn(fr[0]+s[0]*inc, fr[1]+s[1]*inc):
					return False
			return True
		# Now straight-line moves
		if fr[0]==to[0]:
			if fr[1]>to[1]:
				fr, to = to, fr
			for col in range(fr[1]+1,to[1]):
				if self.hasPieceOn(fr[0], col):
					return False
		if fr[1]==to[1]:
			if fr[0]>to[0]:
				fr, to = to, fr
			for row in range(fr[0]+1,to[0]):
				if self.hasPieceOn(row, fr[1]):
					return False
		# Anything else, just return True
		return True

	def getAllPieces(self, colour):
		pieces = []
		for row in range(0, 8):
			for col in range(0, 8):
				if self.hasPieceOn(row, col):
					p = self.getPieceOn([row,col])
					if p.colour==colour:
						pieces.append( [row,col] )
		return pieces

	def getNumPieces(self, colour):
		return len( self.getAllPieces(colour) )
















