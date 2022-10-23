from evaluation import evaluation
def negamax(depth, board):
    if depth == 0:
        finalEval = evaluation(board)
        return -finalEval
    max = float("-inf")
    legalMoves = board.legal_moves
    for move in legalMoves:
        board.push(move)
        score = -negamax(depth - 1, board)
        board.pop()
        if score > max:
            max = score
    return -max