from typing import Optional
from Checkers import Checkers
from Move import Move
from consts import Player

DEPTH_MAX = 4

def eval_board(board: Checkers) -> int:
    score = 0
    for i in range(100):
        score += ((board.white_pawns >> i) & 1) *  1
        score += ((board.white_kings >> i) & 1) *  2
        score += ((board.black_pawns >> i) & 1) * -1
        score += ((board.black_kings >> i) & 1) * -2

    if board.get_current_player() == Player.BLACK:
        score *= -1

    return score

def minimax(board: Checkers, depth: int=0) -> tuple[Optional[Move], int]:
    moves = board.get_moves()
    if depth >= DEPTH_MAX and not [move for move in moves if len(move.takes) > 0]:
        return (None, eval_board(board))

    if not moves:
        return (None, -100)

    best_move, best_score = None, -200
    for move in moves:
        board.make_move(move)

        _, score = minimax(board, depth + 1)
        score *= -1
        if score > best_score:
            best_move = move
            best_score = score

        board.cancel_last_move()

    return (best_move, best_score)


def main():
    board = Checkers()
    board.init_board()
    board.show_board()

    while True:
        input()
        move, score = minimax(board)
        if move == None:
            print("current player has lost")
            break

        print("current player play:", move.origin, move.destination)
        print("evaluation:", score)
        board.make_move(move)
        board.show_board()


if __name__ == "__main__":
    main()
