from Move import Move
from Take import Take
from consts import *

# 10x10, flying king
class Checkers:
    def __init__(self):
        self.white_pawns = 0
        self.white_kings = 0
        self.black_pawns = 0
        self.black_kings = 0
        self.moves = []
    
    def init_board(self):
        # white pawns
        for y in range(4):
            for x in range((y+1)%2, 10, 2):
                self.white_pawns |= 1 << y * 10 + x

        # black pawns
        for y in range(6, 10):
            for x in range((y+1)%2, 10, 2):
                self.black_pawns |= 1 << y * 10 + x

    def show_board(self):
        result = ""
        for y in range(10):
            for x in range(10):
                index = y * 10 + x
                if self.white_pawns & 1 << index:
                    result += "w"
                elif self.white_kings & 1 << index:
                    result += "W"
                elif self.black_pawns & 1 << index:
                    result += "b"
                elif self.black_kings & 1 << index:
                    result += "B"
                else:
                    result += "-"
            result += "\n"
        print(result)

    def make_move(self, move: Move):
        # move the main pawn to its target square
        if move.player == Player.WHITE:
            # if pawn move
            if self.white_pawns & (1 << move.origin):
                self.white_pawns ^= 1 << move.origin
                if move.is_promotion:
                    self.white_kings |= 1 << move.destination
                else:
                    self.white_pawns |= 1 << move.destination
            # if king move
            else:
                self.white_kings ^= 1 << move.origin
                self.white_kings |= 1 << move.destination
        elif move.player == Player.BLACK:
            # if pawn move
            if self.black_pawns & (1 << move.origin):
                self.black_pawns ^= 1 << move.origin
                if move.is_promotion:
                    self.black_kings |= 1 << move.destination
                else:
                    self.black_pawns |= 1 << move.destination
            # if king move
            else:
                self.black_kings ^= 1 << move.origin
                self.black_kings |= 1 << move.destination

        # remove the taken pawns/kings
        for take in move.takes:
            square = 1 << take.index
            if self.white_pawns & square:
                self.white_pawns ^= square
            elif self.white_kings & square:
                self.white_kings ^= square
            if self.black_pawns & square:
                self.black_pawns ^= square
            elif self.black_kings & square:
                self.black_kings ^= square

        self.moves.append(move)
            

def main():
    move1 = Move(Player.WHITE, False, 30, 41, [])
    move2 = Move(Player.BLACK, False, 63, 52, [])
    move3 = Move(Player.WHITE, False, 41, 63, [Take(52, False)])

    board = Checkers()
    board.init_board()
    board.show_board()
    print("-- move 1 --")
    board.make_move(move1)
    board.show_board()
    print("-- move 2 --")
    board.make_move(move2)
    board.show_board()
    print("-- move 3 --")
    board.make_move(move3)
    board.show_board()

if __name__ == "__main__":
    main()
