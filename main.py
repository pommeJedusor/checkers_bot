from Checkers import Checkers
from Minimax import minimax
from Move import Move
import PDN

def does_player_wanna_start() -> bool:
    text = "do you want to start? [Y/n]\n"
    while True:
        response = input(text).lower()
        if response == "y":
            return True
        if response == "n":
            return False
        text = "input not valid\ndo you want to start? [Y/n]\n"

def make_player_move(board: Checkers):
    while True:
        try:
            new_move = input("enter your move:\n")
            PDN.make_PDN_move(board, new_move)
            break
        except:
            print("move not valid, retry")

def main():
    board = Checkers()
    board.init_board()
    board.show_board()

    if does_player_wanna_start():
        make_player_move(board)
 
    while True:
        # bot play
        move, _ = minimax(board)
        if move == None:
            print("you won!")
            break
        board.make_move(move)
        print(PDN.get_move_notation(move))
 
        # player play
        if not board.get_moves():
            print("you lost")
            break
        make_player_move(board)

if __name__ == "__main__":
    main()
