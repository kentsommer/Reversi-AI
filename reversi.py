# Reversi - base code: http://inventwithpython.com/reversi.py

## Author: Kent Sommer 

### Notes: 
## The code to display the game in terminal is from: http://inventwithpython.com/reversi.py
## All AI and alternative evaluation functions were writen by Kent Sommer. 
## The following is a heavily modified version of base. 

import random
import sys

inf = float('inf')

def drawBoard(board):
    # This function prints out the board that it was passed. Returns None.
    SIDELINE = '  +---+---+---+---+---+---+---+---+'
    TBLINE = '  |   |   |   |   |   |   |   |   |'

    print('    1   2   3   4   5   6   7   8')
    print(SIDELINE)
    for y in range(8):
        print(TBLINE)
        print(y+1, end=' ')
        for x in range(8):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(TBLINE)
        print(SIDELINE)


def resetBoard(board):
    # Blanks out the board it is passed, except for the original starting position.
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '

    # Starting pieces:
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'


def getNewBoard():
    # Creates a brand new, blank board data structure.
    board = []
    for i in range(8):
        board.append([' '] * 8)

    return board

def isTerminal(board):
	if getValidMoves(board, computerTile) and getValidMoves(board, playerTile) == []:
		return True
	return False

def maxPlay(board):
	possibleMoves = getValidMoves(board, computerTile)

    #Go through all the possible moves and remember the best scoring moves
	bestScore = -1
	for x, y in possibleMoves:
		dupeBoard = getBoardCopy(board)
		makeMove(dupeBoard, computerTile, x, y)
		score = getScoreOfBoard(dupeBoard)[computerTile]
		if score > bestScore:
			bestMove = [x, y]
			bestScore = score
	return bestMove


def miniMaxValue(board, maxply, best):
	#Implements MiniMax for Reversi AI
	possibleMoves = getValidMoves(board, computerTile)
	if maxply == 0 or isTerminal(board):
		score = getAltScoreOfBoard(board) #[computerTile]
		return score

	#try each move
	for x, y in possibleMoves:
		move = [x,y]
		#print(move)
		dupeBoard = getBoardCopy(board)
		makeMove(dupeBoard, computerTile, x, y)
		value = -1 * miniMaxValue(dupeBoard, maxply-1, best)
		#print(value)
		if best is 0 or value > best:
			best = value
	return best

def miniMax(board, maxply):
	possibleMoves = getValidMoves(board, computerTile)
	best = None

	#try each move
	for x, y in possibleMoves:
		move = [x, y]
		dupeBoard = getBoardCopy(board)
		makeMove(dupeBoard, computerTile, x, y)
		value = -1 * miniMaxValue(dupeBoard, maxply, 0)
		#update best
		if best is None or value > best[0]:
			best = (value, move)
	return best

def alphaBetaValue(board, maxply, alpha, beta):
	possibleMoves = getValidMoves(board, computerTile)

	if maxply == 0 or isTerminal(board):
		return getAltScoreOfBoard(board)[computerTile]

	#try each move
	for x, y in possibleMoves:
		move = [x, y]
		dupeBoard = getBoardCopy(board)
		makeMove(dupeBoard, computerTile, x, y)
		if beta is not None:
			opp_alpha = -1 * beta
		else:
			opp_alpha = None
		if alpha is not None:
			opp_beta = -1 * alpha
		else:
			opp_beta = None
		value = -1 * alphaBetaValue(dupeBoard, maxply-1, opp_alpha, opp_beta)
		#update alpha
		if alpha is -inf or value > alpha:
			alpha = value
		#prune!! ;)
		if (alpha is not None) and (beta is not None) and alpha >= beta:
			return beta
	return alpha

def alphaBeta(board, maxply):
	possibleMoves = getValidMoves(board, computerTile)
	bestScore = 0
	bestMove = []

	#try each move
	for x, y in possibleMoves:
		move = [x, y]
		print("Current Move is: ", move)
		dupeBoard = getBoardCopy(board)
		makeMove(dupeBoard, computerTile, x, y)

		if bestScore is not 0:
			opp_beta = -1 * bestScore
		else:
			opp_beta = inf
		value = -1 * alphaBetaValue(board, maxply, -inf, opp_beta)
		print("Value: ", value)
		#update best
		if bestScore is 0 or value > bestScore:
			if bestScore is 0:
				print("best is 0")
			(bestScore, bestMove) = (value, move)
			print("BestScore is:", bestScore)
	print(bestMove)
	print(bestScore)
	return (bestScore, bestMove)

def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection # first step in the direction
        y += ydirection # first step in the direction
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y): # break out of while loop, then continue in for loop
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = ' ' # restore the empty space
    if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= 7 and y >= 0 and y <=7


def getBoardWithValidMoves(board, tile):
    # Returns a new board with . marking the valid moves the given player can make.
    dupeBoard = getBoardCopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'
    return dupeBoard


def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves


def getScoreOfBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}


def getAltScoreOfBoard(board):
	# A "Hopefully" better evaluation function
    p = 0
    c = 0
    l = 0
    m = 0
    f = 0
    d = 0
    compT = 0
    playT = 0
    compFT = len(getValidMoves(board, computerTile))
    playFT = len(getValidMoves(board, playerTile))

    for x in range(8):
        for y in range(8):
            if board[x][y] == computerTile:
                d += 1
                compT += 1
            elif board[x][y] == playerTile:
                d -= 1
                playT += 1

    if compT > playT:
    	p = (100 * compT)/(compT + playT)
    elif compT < playT:
    	p = -(100 * playT)/(compT + playT)
    else:
    	p = 0

    if compFT > playFT:
        f = (100 * compFT)/(compFT + playFT)
    elif compFT < playFT:
        f = -(100 * playFT)/(compFT + playFT)
    else:
        f = 0

	# Corner Occupancy
    compT = 0
    playT = 0
    if board[0][0] == computerTile:
        compT += 1
    if board[0][0] == playerTile:
        playT += 1
    if board[0][7] == computerTile:
        compT += 1
    if board[0][7] == playerTile:
        playT += 1
    if board[7][0] == computerTile:
        compT += 1
    if board[7][0] == playerTile:
        playT += 1
    if board[7][7] == computerTile:
        compT += 1
    if board[7][7] == playerTile:
        playT += 1
    c = 25 * (compT - playT)

	#Corner Closeness
    compT = 0
    playT = 0
	# Square 0... ha ha ha
    if isValidMove(board, computerTile, 0, 0) and isValidMove(board, playerTile, 0, 0) != False:
        if board[0][1] == computerTile:
            compT += 1
        elif board[0][1] == playerTile:
            playT += 1
        if board[1][1] == computerTile:
            compT += 1
        elif board[1][1] == playerTile:
            playT += 1
        if board[1][0] == computerTile:
            compT += 1
        elif board[1][0] == playerTile:
            playT += 1

	#square [0][7]
    if isValidMove(board, computerTile, 0, 7) and isValidMove(board, playerTile, 0, 7) != False:
        if board[0][6] == computerTile:
            compT += 1
        elif board[0][6] == playerTile:
            playT += 1
        if board[1][6] == computerTile:
            compT += 1
        elif board[1][6] == playerTile:
            playT += 1
        if board[1][7] == computerTile:
            compT += 1
        elif board[1][7] == playerTile:
            playT += 1

	#square [7][0]
    if isValidMove(board, computerTile, 7, 0) and isValidMove(board, playerTile, 7, 0) != False:
        if board[7][1] == computerTile:
            compT += 1
        elif board[7][1] == playerTile:
            playT += 1
        if board[6][1] == computerTile:
            compT += 1
        elif board[6][1] == playerTile:
            playT += 1
        if board[6][0] == computerTile:
            compT += 1
        elif board[6][0] == playerTile:
            playT += 1

	#square [7][7]
    if isValidMove(board, computerTile, 7, 7) and isValidMove(board, playerTile, 7, 7) != False:
        if board[6][7] == computerTile:
            compT += 1
        elif board[6][7] == playerTile:
            playT += 1
        if board[6][6] == computerTile:
            compT += 1
        elif board[6][6] == playerTile:
            playT += 1
        if board[7][6] == computerTile:
            compT += 1
        elif board[7][6] == playerTile:
            playT += 1
    l = -12.5 * (compT - playT)

	#Mobility
    compT = compFT
    playT = playFT
    if compT > playT:
        m = (100 * compT)/(compT + playT)
    elif compT < playT:
        m = -(100 * playT)/(compT + playT)
    else:
        m = 0

	#calculate board score
    score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)
    return score




def enterPlayerTile():
    # Let's the player type which tile they want to be.
    # Returns a list with the player's tile as the first item, and the computer's tile as the second.
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()

    # the first element in the tuple is the player's tile, the second is the computer's tile.
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():
    # Randomly choose the player who goes first.
	return 'player'



def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def makeMove(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def getBoardCopy(board):
    # Make a duplicate of the board list and return the duplicate.
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]

    return dupeBoard


def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


def getPlayerMove(board, playerTile):
    # Let the player type in their move.
    # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, or type quit to end the game, or hints to turn off/on hints.')
        move = input().lower()
        if move == 'quit':
            return 'quit'
        if move == 'hints':
            return 'hints'

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
            print('For example, 81 will be the top-right corner.')

    return [x, y]


def getComputerMove(board, computerTile):
	#get list of possible moves for computer
	possibleMoves = getValidMoves(board, computerTile)
    # always go for a corner if available.

	for x, y in possibleMoves:
		if isOnCorner(x, y):
			print("Placed on a corner")
			return [x, y]

	return miniMax(board, 3)[1]
	#return alphaBeta(board, 3)[1]
    #return maxPlay(board)


def showPoints(playerTile, computerTile):
    # Prints out the current score.
    scores = getScoreOfBoard(mainBoard)
    print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))



print('Welcome to Reversi!')

while True:
    # Reset the board and game.
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()
    showHints = False
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')

    while True:
        if turn == 'player':
            # Player's turn.
            if showHints:
                validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                drawBoard(validMovesBoard)
            else:
                drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            move = getPlayerMove(mainBoard, playerTile)
            if move == 'quit':
                print('Thanks for playing!')
                sys.exit() # terminate the program
            elif move == 'hints':
                showHints = not showHints
                continue
            else:
                makeMove(mainBoard, playerTile, move[0], move[1])

            if getValidMoves(mainBoard, computerTile) == []:
                break
            else:
                turn = 'computer'

        else:
            # Computer's turn.
            drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            input('Press Enter to see the computer\'s move.')
            x, y = getComputerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, x, y)

            if getValidMoves(mainBoard, playerTile) == []:
                break
            else:
                turn = 'player'

    # Display the final score.
    drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard)
    print('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))
    if scores[playerTile] > scores[computerTile]:
        print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
    else:
        print('The game was a tie!')

    if not playAgain():
        break
