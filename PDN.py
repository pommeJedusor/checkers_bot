from Checkers import Checkers
from Move import Move


def get_move_notation(move: Move) -> str:
    start = 50 - (move.origin // 2)
    end   = 50 - (move.destination // 2)
    middle = "-" if not move.takes else "x"
    return f"{start}{middle}{end}"

def get_PDN(board: Checkers) -> str:
    moves = [get_move_notation(move) for move in board.moves]
    pdn = ""
    for i, move in enumerate(moves):
        if i == 0:
            pdn += "1."
        elif i % 2 == 0:
            pdn += f" {i//2+1}."
        pdn += f" {move}"

    return pdn
