# 10x10, flying king
class Checkers:
    def __init__(self):
        self.white_pawns = 0
        self.white_kings = 0
        self.black_pawns = 0
        self.black_kings = 0
    
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

def main():
    board = Checkers()
    board.init_board()
    board.show_board()

if __name__ == "__main__":
    main()
