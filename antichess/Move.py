import Pieces

class MoveViolation(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

rowNotation = "87654321"
colNotation = "abcdefgh"

class Move:
	fr = [0, 0]
	to = [0, 0]
	def __init__(self, fr, to):
		self.fr = fr
		self.to = to
        @staticmethod
        def fromNotation(m, colour):
            try:
	        mm = [m[0:2], m[2:4]]   # e.g. e2e4
                fr = [0, 0]
	        to = [0, 0]
	        conv = dict(a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7)
	        fr[1] = conv[ mm[0][0] ]
	        fr[0] = 7 - (int(mm[0][1]) - 1)
	        to[1] = conv[ mm[1][0] ]
	        to[0] = 7 - (int(mm[1][1]) - 1)
	        # Promotion?
	        promotionDict = dict(Q=Pieces.Queen(colour), R=Pieces.Rook(colour), N=Pieces.Knight(colour), B=Pieces.Bishop(colour), K=Pieces.King(colour))
	        if len(m)>4:
	    	    return PromotionMove( fr, to, promotionDict[m[4]] )
	        else:
	    	    return Move(fr, to)
            except Exception as e:
                print e
                raise

	def __getitem__(self, k):
		if k==0:
			return self.fr
		if k==1:
			return self.to
		raise MoveViolation("Syntax move[k] only valid for k=0,1")
	def unpack(self):
		return self.fr[0]*8 + self.fr[1], self.to[0]*8 + self.to[1]
	def __str__(self):
		rowf = self.fr[0]
		colf = self.fr[1]
		rowt = self.to[0]
		colt = self.to[1]
		return colNotation[colf]+rowNotation[rowf]+colNotation[colt]+rowNotation[rowt]

class PromotionMove(Move):
	promoteTo = None
	def __init__(self, fr, to, promoteTo):
		Move.__init__(self, fr, to)
		self.promoteTo = promoteTo
	def __str__(self):
		return Move.__str__(self) + self.promoteTo.symbol

class PassMove(Move):
	def __init__(self):
		pass
	def __str__(self):
		return "PASS"

class ResignMove(Move):
	def __init__(self):
		pass
	def __str__(self):
		return "RESIGN"

class RetractMove(Move):
	def __init__(self):
		pass
	def __str__(self):
		return "RETRACT"

class NoneMove(Move):
	def __init__(self):
		Move.__init__(self, [-1,-1], [-1,-1])
	def __str__(self):
		return "NONE"

PASS = PassMove()
RESIGN = ResignMove()
RETRACT = RetractMove()
NONE = NoneMove()
