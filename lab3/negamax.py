from evaluation import evaluation

def negamax(depth, board):
    max = float("-inf")

    if depth == 0:
        return evaluation(board)

    for move in board.legal_moves:
        board.push(move)
        score = -negamax(depth - 1, board)

        board.pop()
        if score > max:
            max = score
            
    return max