import sys, getopt
import chess
import chess.svg
from chessboard import display
from evaluation import evaluation
from negamax import negamax
from negascout import negascout
from pvs import pvs
import time
import random

board = chess.Board()
displayBord = display.start()
INF = float("inf")
DEPTH = 2
SEARCH_FUNC = "negamax"
SLEEP_TIME = 0.25

def endCondition(board, color):
    if board.is_checkmate():
        print(color + ' win')
        svg = chess.svg.board(board)
        with open('endGameBoard.svg', 'w') as file:
            file.write(svg)
        exit()
    if board.is_fivefold_repetition():
        print('Process stuck')
        exit()
    time.sleep(SLEEP_TIME)

def bestMove(depth, board, searchfunc):
    legalMoves = board.legal_moves
    bestMove = None
    maxScore = -INF
    randomList = []

    for move in legalMoves:
        board.push(move)

        match searchfunc:
            case 'negamax':
                score = negamax(depth - 1, board)
            case 'negascout':
                score = negascout(depth - 1, board, -INF, INF)
            case 'pvs':
                score = pvs(depth - 1, board, -INF, INF)
            case _:
                print("Repeat!")
                exit()
        board.pop()
        if score >= maxScore:
            if score == maxScore:
                randomList.append(move)
                # randomList.append(str(move.uci())+'('+str(score)+')')
                # print('add='+str(randomList))
            else:
                randomList.clear()
                randomList.append(move)
                # randomList.append(str(move.uci())+'('+str(score)+')')
                # print('clear='+str(randomList))
            maxScore = score
            bestMove = move
    if len(randomList) > 0:
        bestMove = random.choice(randomList)
    # print('\n')
    # print('list='+str(randomList))
    # print('random='+str(k33))
    # print('\n')
    return bestMove

def main(args):
    board = chess.Board()
    options, arguments = getopt.getopt(args,"f:",["function="])
    for option, argument in options:
        if option in ("-f", "--function"):
            SEARCH_FUNC = argument

    while True:
        newbestMove = bestMove(DEPTH, board, SEARCH_FUNC)
        print('White move: ' + board.san(newbestMove))
        board.push(newbestMove)

        display.check_for_quit()
        display.update(board.fen(), displayBord)

        endCondition(board, 'Black')

        newbestMove = bestMove(DEPTH, board, SEARCH_FUNC)
        print('Black move: ' + board.san(newbestMove))
        board.push(newbestMove)

        display.check_for_quit()
        display.update(board.fen(), displayBord)

        endCondition(board, 'White')

if __name__ == "__main__":
   main(sys.argv[1:])