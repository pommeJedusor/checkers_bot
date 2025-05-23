from typing import Optional
from Checkers import Checkers
from Move import Move
from consts import Player
import PDN

DEPTH_MAX = 7


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
        score += ((board.white_pawns >> i) & 1) * 1
        score += ((board.white_kings >> i) & 1) * 2
        score += ((board.black_pawns >> i) & 1) * -1
        score += ((board.black_kings >> i) & 1) * -2

    if board.get_current_player() == Player.BLACK:
        score *= -1

    return score


def minimax(
    board: Checkers,
    depth: int = 0,
    alpha: int = -1000,
    beta: int = 1000,
    explored_positions=None,
) -> tuple[Optional[Move], int]:
    # if explored_positions == None:
    #    explored_positions = {}
    # hash = get_hash(board)
    # if hash in explored_positions:
    #    alpha = max(alpha, explored_positions[hash])
    # else:
    #    explored_positions[hash] = -1000

    moves = board.get_moves()
    if depth >= DEPTH_MAX and not [move for move in moves if len(move.takes) > 0]:
        score = eval_board(board)
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

        # explored_positions[hash] = max(score, explored_positions[hash] or -1000)
        alpha = max(alpha, score)
        if alpha >= beta:
            break

    return (best_move, best_score)


def main():
    board = PDN.get_board_from_PDN(
        "1. 33-28 20-25 2. 34-30 25x34 3. 40x29 19-24 4. 29x20 15x24 5. 39-33 18-22 6. 44-39 24-29 7. 33x24 22x44 8. 50x39 17-22 9. 39-33 16-21 10. 33-28 22x33 11. 38x29 21-26 12. 32-28 14-19 13. 35-30 12-18 14. 28-23 19x28 15. 37-32 28x37 16. 41x32 26x28 17. 29-23 18x20 18. 43-39 28-32 19. 49-43 20-25 20. 43-38 32x34 21. 30x39 25-30 22. 45-40 30-35 23. 40-34 13-19 24. 42-38 19-24 25. 34-30 24-29 26. 39-33 35x24 27. 48-43 29-34 28. 47-42 34-40 29. 42-37 40-45 30. 37-32 45-50 31. 46-41"
    )
    board.show_board()
    for move in board.get_moves():
        # I play: ['5017', '1748', '4835']
        print(move.origin, move.destination)
        for take in move.takes:
            print(take.index)
        print(PDN.get_lidraughts_move_notation_str(move))


if __name__ == "__main__":
    main()
