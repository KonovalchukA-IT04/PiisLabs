from evaluation import evaluation

def pvs(depth, board, alpha, beta):
    bestScore = float("-inf")
    b = beta
    if depth == 0:
        return evaluation(board)

    for move in board.legal_moves:
        board.push(move)
        score = -pvs(depth - 1, board, -b, -alpha)
        
        if score > bestScore:
            if alpha < score < beta:
                bestScore = max(score, bestScore)
            else:
                bestScore = -pvs(depth - 1, board, -beta, -score)

        board.pop()
        
        if alpha > beta:
            return alpha
        b = alpha + 1

    return bestScore