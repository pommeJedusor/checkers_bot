from typing import Optional
from Checkers import Checkers
from Move import Move
from consts import Player
import PDN

DEPTH_MAX = 1

def get_hash(board: Checkers) -> int:
    white_hash = board.white_pawns | (board.white_kings >> 1)
    black_hash = board.black_pawns | (board.black_kings >> 1)
    final_hash = white_hash | (black_hash << 100)
    if board.get_current_player() == Player.WHITE:
        final_hash |= 1 << 200
    return final_hash

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

def minimax(board: Checkers, depth: int=0, alpha: int=-1000, beta: int=1000, explored_positions=None) -> tuple[Optional[Move], int]:
    #if explored_positions == None:
    #    explored_positions = {}
    #hash = get_hash(board)
    #if hash in explored_positions:
    #    return (None, explored_positions[hash])

    moves = board.get_moves()
    if depth >= DEPTH_MAX and not [move for move in moves if len(move.takes) > 0]:
        score = eval_board(board)
        #explored_positions[hash] = score
        return (None, score)

    if not moves:
        return (None, -100)

    best_move, best_score = None, -200
    for move in moves:
        board.make_move(move)

        _, score = minimax(board, depth + 1, -beta, -alpha, explored_positions)
        score *= -1

        board.cancel_last_move()

        if score > best_score:
            best_move = move
            best_score = score

        alpha = max(alpha, score)
        if alpha >= beta:
            break

    #explored_positions[hash] = best_score
    return (best_move, best_score)


def main():
    board = Checkers()
    board.init_board()
    board.show_board()

    while True:
        move, _ = minimax(board)
        if move == None:
            print("current player has lost")
            break

        board.make_move(move)
        print(PDN.get_move_notation(move))
        new_move = input("enter your move:\n")
        PDN.make_PDN_move(board, new_move)

if __name__ == "__main__":
    main()
