#!/usr/bin/python 

#from rules import suicide
import Board
import Player
import Rules
import Move

from optparse import OptionParser
#import argparse # python 2.7

playerNames = ["White", "Black"]


if __name__=="__main__":

	parser = OptionParser()
	parser.add_option("-d", "--depth", type="int", dest="AIdepth", default=0,
	                  help="set initial AI search depth", metavar="DEPTH")
	parser.add_option("-w", "--white", dest="white", default="human",
	                  help="set white player", metavar="PLAYER")
	parser.add_option("-b", "--black", dest="black", default="ai",
	                  help="set black player", metavar="PLAYER")
	(options, args) = parser.parse_args()

	b = Board.Board()
	AIdepth = options.AIdepth

	playertype = [options.white, options.black]
	players = []
	for i in [0,1]:
		p = playertype[i]
		if p=="human":
			players.append( Player.HumanPlayer(i) )
		elif p=="ai":
			players.append( Player.AIPlayer(i, AIdepth) )
		elif p=="random":
			players.append( Player.RandomPlayer(i) )
		elif p=="pass":
			players.append( Player.PassingPlayer(i) )
		else:
			#TODO exception
			print "Error: unknown player type:", p
			exit()

		print "%s is %s." % (playerNames[i], players[i].name),
		if p=="ai":
			print "Depth is %s." % AIdepth
		print ""


	r = Rules.Suicide()
	b.displayAsText()
	print ""

	WIN = -1
	while True:
		for col in [0, 1]:
			# First check for win
			numpieces = b.getNumPieces(col)
			valid, capture = r.getAllValidMoves(b, col)
			if numpieces==0 or len(valid)==0:
				WIN = col
				break

			madeValidMove = False;
			while not madeValidMove:
                                print playerNames[col] + "'s turn"
				m = players[col].getMove(b)
                                # If retract, we pop two moves and try again
                                if m==Move.RETRACT:
                                    lastMoveByThisPlayer = b.getSecondLastMove()
                                    if b.retractTurn():
                                        print playerNames[col], "retracts move", lastMoveByThisPlayer
                                    else:
                                        print "Unable to retract."
			            print ""
                                    b.displayAsText()
			            print ""
                                    continue
				try:
					r.validate(m, b, col)
					madeValidMove = True
				except Rules.RulesViolation as e:
					madeValidMove = False
					print "Invalid move: " + e.value
			if m==Rules.Move.RESIGN:
				print playerNames[col] + " resigns. "
				WIN = 1-col
				break
			b.makeMove(m)
			print ""
			b.displayAsText()
			print playerNames[col] + " moved", m
			print ""
		if not WIN==-1:
			print playerNames[WIN] + " wins!"
			exit()






