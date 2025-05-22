from Checkers import Checkers
from Move import Move
import re


def get_move_notation(move: Move) -> str:
    start = 50 - (move.origin // 2)
    end = 50 - (move.destination // 2)
    middle = "-" if not move.takes else "x"
    return f"{start}{middle}{end}"


def get_lidraughts_move_notation_list(move: Move) -> list[str]:
    if len(move.takes) < 2:
        start = str(50 - (move.origin // 2))
        end = str(50 - (move.destination // 2))
        start = "0" * (2 - len(start)) + start
        end = "0" * (2 - len(end)) + end
        return [f"{start}{end}"]

    result = []
    previous = str(50 - (move.origin // 2))
    previous = "0" * (2 - len(previous)) + previous
    for square in move.passing_by:
        square = str(50 - (square // 2))
        square = "0" * (2 - len(square)) + square
        result.append(f"{previous}{square}")
        previous = square

    return result


def get_lidraughts_move_notation_str(move: Move) -> str:
    if len(move.takes) < 2:
        start = str(50 - (move.origin // 2))
        end = str(50 - (move.destination // 2))
        start = "0" * (2 - len(start)) + start
        end = "0" * (2 - len(end)) + end
        return f"{start}{end}"

    result = ""
    for square in [move.origin] + move.passing_by:
        str_square = str(50 - (square // 2))
        result += "0" * (2 - len(str_square)) + str_square

    return result


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


def make_PDN_move(board: Checkers, move: str):
    for m in board.get_moves():
        if move == get_move_notation(m):
            board.make_move(m)
            return

    raise Exception("PDN move not found")


def make_lidraughts_move(board: Checkers, move: str):
    print("start make_lidraughts_move")
    for m in board.get_moves():
        print(move, get_lidraughts_move_notation_str(m))
        if move == get_lidraughts_move_notation_str(m):
            board.make_move(m)
            print("end make_lidraughts_move")
            return

    print("end make_lidraughts_move")
    raise Exception("lidraughts move not found")


def get_board_from_PDN(pdn: str) -> Checkers:
    board = Checkers()
    board.init_board()

    new_turn_pattern = re.compile("^\d+\.$")

    for move in pdn.split(" "):
        if not new_turn_pattern.match(move):
            make_PDN_move(board, move)

    return board


def main():
    board = get_board_from_PDN(
        "1. 35-30 20-25 2. 40-35 19-24 3. 30x19 14x23 4. 45-40 18-22 5. 50-45 23-28 6. 32x23 22-27 7. 31x22 17x19 8. 38-32 19-24 9. 43-38 16-21 10. 49-43 21-26 11. 36-31 15-20 12. 41-36 13-19 13. 47-41 12-18 14. 34-30 25x34 15. 40x29 20-25 16. 29x20 25x14 17. 45-40 19-24 18. 40-34 18-23 19. 44-40 14-19 20. 34-30 11-17"
    )
    board.show_board()


if __name__ == "__main__":
    main()
