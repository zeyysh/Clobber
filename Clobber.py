# AI Clobber project
# Zeynab Shiri
# 9705253

import copy
import pygame
import random
import sys
import time

from pygame.locals import *

FPS = 10  # frames per second to update the screen
WINDOWWIDTH = 640  # width of the program's window, in pixels
WINDOWHEIGHT = 480  # height in pixels
SPACESIZE = 50  # width & height of each space on the board, in pixels
BOARDWIDTH = 5  # how many columns of spaces on the game board
BOARDHEIGHT = 6  # how many rows of spaces on the game board
WHITE_TILE = 'WHITE_TILE'  # an arbitrary but unique value
BLACK_TILE = 'BLACK_TILE'  # an arbitrary but unique value
EMPTY_SPACE = 'EMPTY_SPACE'  # an arbitrary but unique value
RESULT = 0
ANIMATIONSPEED = 10  # integer from 1 to 100, higher is faster animation

# Amount of space on the left & right side (XMARGIN) or above and below
# (YMARGIN) the game board, in pixels.
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)

#              R    G    B
WHITE = (51, 0, 102)
BLACK = (0, 0, 0)
GREEN = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
BROWN = (174, 94, 0)

TEXTBGCOLOR1 = BRIGHTBLUE
TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
HINTCOLOR = BROWN


def main():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE

    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Clobber')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)

    # Set up the background image.
    boardImage = pygame.image.load('ugly_back.png')
    # Use smoothscale() to stretch the board image to fit the entire board:
    boardImage = pygame.transform.smoothscale(boardImage, (BOARDWIDTH * SPACESIZE, BOARDHEIGHT * SPACESIZE))
    boardImageRect = boardImage.get_rect()
    boardImageRect.topleft = (XMARGIN, YMARGIN)
    BGIMAGE = pygame.image.load('bg.png')
    # Use smoothscale() to stretch the background image to fit the entire window:
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    BGIMAGE.blit(boardImage, boardImageRect)

    # Run the main game.
    while True:
        if runGame() == False:
            break


def runGame():
    # Reset the board and game.
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    showHints = False
    turn = 'player'
    dark_Img = pygame.image.load('55.png')
    light_Img = pygame.image.load('5.png')

    # Draw the starting board and ask the player what color they want.
    drawBoard(dark_Img, light_Img, mainBoard)
    playerTile, computerTile = enterPlayerTile()

    # Make the Surface and Rect objects for the "New Game"
    newGameSurf = FONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR2)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (WINDOWWIDTH - 8, 10)

    while True:  # main game loop
        # Keep looping for player and computer's turns.
        if turn == 'player':
            # Player's turn:
            if getValidMoves(mainBoard, playerTile) == []:
                # If it's the player's turn but they
                # can't move, then end the game.
                break
            movexy = None
            while movexy == None:
                # Keep looping until the player clicks on a valid space.

                # Determine which board data structure to use for display.
                if showHints:
                    boardToDraw = getBoardWithValidMoves(mainBoard, playerTile)
                else:
                    boardToDraw = mainBoard

                checkForQuit()
                for event in pygame.event.get():  # event handling loop
                    if event.type == MOUSEBUTTONUP:
                        # Handle mouse click events
                        mousex, mousey = event.pos
                        if newGameRect.collidepoint((mousex, mousey)):
                            # Start a new game
                            return True
                        # movexy is set to a two-item tuple XY coordinate, or None value
                        movexy = getSpaceClicked(mousex, mousey)
                        if (movexy != None and mainBoard[movexy[0]][movexy[1]] == EMPTY_SPACE) or (
                                movexy != None and mainBoard[movexy[0]][movexy[1]] == computerTile):
                            movexy = None

                # Draw the game board.
                drawBoard(dark_Img, light_Img, boardToDraw)
                drawInfo(boardToDraw, playerTile, computerTile, turn)

                # Draw the "New Game" buttons.
                DISPLAYSURF.blit(newGameSurf, newGameRect)

                MAINCLOCK.tick(FPS)
                pygame.display.update()

            movexy_second = None
            while movexy_second == None:
                # Keep looping until the player clicks on a valid space.

                # Determine which board data structure to use for display.
                if showHints:
                    boardToDraw = getBoardWithValidMoves(mainBoard, playerTile)
                else:
                    boardToDraw = mainBoard

                checkForQuit()
                for event in pygame.event.get():  # event handling loop
                    if event.type == MOUSEBUTTONUP:
                        # Handle mouse click events
                        mousex, mousey = event.pos
                        if newGameRect.collidepoint((mousex, mousey)):
                            # Start a new game
                            return True
                        # movexy is set to a two-item tuple XY coordinate, or None value
                        movexy_second = getSpaceClicked(mousex, mousey)
                        if movexy_second != None and not isValidMove(mainBoard, playerTile, movexy_second[0],
                                                                     movexy_second[1]) or mainBoard[movexy_second[0]][
                            movexy_second[1]] != computerTile:
                            movexy_second = None

            # Make the move and end the turn.
            makeMove(mainBoard, playerTile, movexy[0], movexy[1], movexy_second[0], movexy_second[1], True)

            if getValidMoves(mainBoard, playerTile) == []:
                # If it was set to be the computer's turn but
                # they can't move, then end the game.
                break

            if getValidMoves(mainBoard, computerTile) != []:
                # Only set for the computer's turn if it can make a move.
                turn = 'computer'

        else:
            # Computer's turn:
            if getValidMoves(mainBoard, computerTile) == []:
                # If it was set to be the computer's turn but
                # they can't move, then end the game.
                break

            # Draw the board.
            drawBoard(dark_Img, light_Img, mainBoard)
            drawInfo(mainBoard, playerTile, computerTile, turn)

            # Draw the "New Game" buttons.
            DISPLAYSURF.blit(newGameSurf, newGameRect)

            # Make it look like the computer is thinking by pausing a bit.
            pauseUntil = time.time() + random.randint(5, 15) * 0.1
            while time.time() < pauseUntil:
                pygame.display.update()

            # Make the move and end the turn.
            x, y, xend, yend = getComputerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, x, y, xend, yend, True)
            if getValidMoves(mainBoard, computerTile) == []:
                # If it was set to be the computer's turn but
                # they can't move, then end the game.
                break
            if getValidMoves(mainBoard, playerTile) != []:
                # Only set for the player's turn if they can make a move.
                turn = 'player'
            else:
                break

    # Display the final score.
    drawBoard(dark_Img, light_Img, mainBoard)
    scores = getScoreOfBoard(mainBoard)

    # Determine the text of the message to display.
    if turn == 'player':
        text = 'You win! Congratulations!'
    else:
        text = 'You lost.'

    textSurf = FONT.render(text, True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(textSurf, textRect)

    # Display the "Play again?" text with Yes and No buttons.
    text2Surf = BIGFONT.render('Play again?', True, TEXTCOLOR, TEXTBGCOLOR1)
    text2Rect = text2Surf.get_rect()
    text2Rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 50)

    # Make "Yes" button.
    yesSurf = BIGFONT.render('Yes', True, TEXTCOLOR, TEXTBGCOLOR1)
    yesRect = yesSurf.get_rect()
    yesRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 90)

    # Make "No" button.
    noSurf = BIGFONT.render('No', True, TEXTCOLOR, TEXTBGCOLOR1)
    noRect = noSurf.get_rect()
    noRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 90)

    while True:
        # Process events until the user clicks on Yes or No.
        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if yesRect.collidepoint((mousex, mousey)):
                    return True
                elif noRect.collidepoint((mousex, mousey)):
                    return False
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(text2Surf, text2Rect)
        DISPLAYSURF.blit(yesSurf, yesRect)
        DISPLAYSURF.blit(noSurf, noRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)


def translateBoardToPixelCoord(x, y):
    return XMARGIN + x * SPACESIZE + int(SPACESIZE / 2), YMARGIN + y * SPACESIZE + int(SPACESIZE / 2)


def drawBoard(dark_Img, light_Img, board):
    # Draw background of board.
    DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())
    # Draw the black & white tiles.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            centerx, centery = translateBoardToPixelCoord(x, y)
            if board[x][y] == WHITE_TILE or board[x][y] == BLACK_TILE:
                if board[x][y] == WHITE_TILE:
                    player(light_Img, centerx - 18, centery - 18)
                else:
                    player(dark_Img, centerx - 18, centery - 18)


def player(playerImg, x, y):
    DISPLAYSURF.blit(playerImg, (x, y))


def getSpaceClicked(mousex, mousey):
    # Return a tuple of two integers of the board space coordinates where
    # the mouse was clicked. (Or returns None not in any space.)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if mousex > x * SPACESIZE + XMARGIN and \
                    mousex < (x + 1) * SPACESIZE + XMARGIN and \
                    mousey > y * SPACESIZE + YMARGIN and \
                    mousey < (y + 1) * SPACESIZE + YMARGIN:
                return (x, y)
    return None


def drawInfo(board, playerTile, computerTile, turn):
    # Draws scores and whose turn it is at the bottom of the screen.
    turns = getScoreOfBoard(board)
    turnSurf = FONT.render("Player turn:%s " % (str(turn.title())), True, TEXTCOLOR)
    turnRect = turnSurf.get_rect()
    turnRect.bottomleft = (80, WINDOWHEIGHT - 5)
    DISPLAYSURF.blit(turnSurf, turnRect)


def resetBoard(board):
    counter = 0
    for j in range(BOARDHEIGHT):
        for i in range(BOARDWIDTH):
            if counter % 2 == 0:
                board[i][j] = WHITE_TILE
            else:
                board[i][j] = BLACK_TILE
            counter += 1


def getNewBoard():
    # Creates a brand new, empty board data structure.
    board = []
    for i in range(BOARDWIDTH):
        board.append([EMPTY_SPACE] * BOARDHEIGHT)

    return board


def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move is invalid. If it is a valid
    # move, returns a list of spaces of the captured pieces.
    if board[xstart][ystart] == EMPTY_SPACE or not isOnBoard(xstart, ystart):
        return False
    temp = board[xstart][ystart]

    if temp == WHITE_TILE:
        otherTile = BLACK_TILE
    else:
        otherTile = WHITE_TILE

    tilesToFlip = []
    # check each of the eight directions:
    for xdirection, ydirection in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # The piece belongs to the other player next to our piece.
            tilesToFlip.append([x, y])

    board[xstart][ystart] = temp  # make space empty
    if len(tilesToFlip) == 0:  # If no tiles flipped, this move is invalid
        return False
    return tilesToFlip


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x < BOARDWIDTH and y >= 0 and y < BOARDHEIGHT


def getBoardWithValidMoves(board, tile):
    # Returns a new board with hint markings.
    dupeBoard = copy.deepcopy(board)

    return dupeBoard


def getValidMoves(board, tile):
    # Returns a list of (x,y) tuples of all valid moves.
    validMoves = []

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append((x, y))
    return validMoves


def getScoreOfBoard(board):
    # Determine the score by Submission the tiles.
    xscore = len(getBoardWithValidMoves(board, WHITE_TILE))
    oscore = len(getBoardWithValidMoves(board, BLACK_TILE))
    result = xscore - oscore

    return {WHITE_TILE: xscore, BLACK_TILE: oscore, RESULT: result}


def enterPlayerTile():
    # Draws the text and handles the mouse click events for letting
    # the player choose which color they want to be.  Returns
    # [WHITE_TILE, BLACK_TILE] if the player chooses to be White,
    # [BLACK_TILE, WHITE_TILE] if Black.

    # Create the text.
    textSurf = FONT.render('Do you want to be brown or red?', True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    xSurf = BIGFONT.render('Brown', True, TEXTCOLOR, TEXTBGCOLOR1)
    xRect = xSurf.get_rect()
    xRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 40)

    oSurf = BIGFONT.render('Red', True, TEXTCOLOR, TEXTBGCOLOR1)
    oRect = oSurf.get_rect()
    oRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 40)

    while True:
        # Keep looping until the player has clicked on a color.
        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint((mousex, mousey)):
                    return [WHITE_TILE, BLACK_TILE]
                elif oRect.collidepoint((mousex, mousey)):
                    return [BLACK_TILE, WHITE_TILE]

        # Draw the screen.
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(oSurf, oRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)


def makeMove(board, tile, xstart, ystart, xend, yend, realMove=False):
    # Place the tile on the board at xstart, ystart, and flip tiles
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = EMPTY_SPACE
    board[xend][yend] = tile
    return True


def getComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.

    # randomize the order of the possible moves

    # Go through all possible moves and remember the best scoring move
    bestScore = -1
    bestMove = [0, 0, 0, 0]
    for y in range(BOARDHEIGHT):
        for x in range(BOARDWIDTH):
            if board[x][y] == computerTile:
                dupeBoard = copy.deepcopy(board)
                possible_moves = isValidMove(board, computerTile, x, y)
                if not possible_moves:
                    continue
                for xend, yend in possible_moves:
                    makeMove(dupeBoard, computerTile, x, y, xend, yend)
                    score = getScoreOfBoard(dupeBoard)[RESULT]
                    if score > bestScore:
                        bestMove = [x, y, xend, yend]
                        bestScore = score
    return bestMove


def checkForQuit():
    for event in pygame.event.get((QUIT, KEYUP)):  # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()
