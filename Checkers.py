from typing import Optional
from Move import Move
from Take import Take
from consts import *
import random

def is_promotion(y: int, player: Player) -> bool:
    return y == 9 and player == Player.WHITE or y == 0 and player == Player.BLACK

# 10x10, flying king
class Checkers:
    def __init__(self):
        self.white_pawns = 0
        self.white_kings = 0
        self.black_pawns = 0
        self.black_kings = 0
        self.moves: list[Move] = []

    def get_current_player(self) -> Player:
        if not self.moves or self.moves[-1].player == Player.BLACK:
            return Player.WHITE
        return Player.BLACK
    
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

    def cancel_last_move(self):
        move = self.moves.pop()

        # move the main pawn to its original square
        if move.player == Player.WHITE:
            if self.white_pawns & (1 << move.destination):
                self.white_pawns ^= 1 << move.destination
                self.white_pawns |= 1 << move.origin
            else:
                self.white_kings ^= 1 << move.destination
                if move.is_promotion:
                    self.white_pawns |= 1 << move.origin
                else:
                    self.white_kings |= 1 << move.origin
        if move.player == Player.BLACK:
            if self.black_pawns & (1 << move.destination):
                self.black_pawns ^= 1 << move.destination
                self.black_pawns |= 1 << move.origin
            else:
                self.black_kings ^= 1 << move.destination
                if move.is_promotion:
                    self.black_pawns |= 1 << move.origin
                else:
                    self.black_kings |= 1 << move.origin

        # put back the taken pawns/kings
        for take in move.takes:
            square = 1 << take.index
            if move.player == Player.BLACK and not take.is_king:
                self.white_pawns |= square
            elif move.player == Player.BLACK and take.is_king:
                self.white_kings |= square
            elif move.player == Player.WHITE and not take.is_king:
                self.black_pawns |= square
            elif move.player == Player.WHITE and take.is_king:
                self.black_kings |= square

    def _get_pawn_takes(self, player: Player, index: int, _previous_takes: Optional[set[int]]=None, _moves: Optional[list[Move]]=None) -> list[Move]:
        previous_takes = _previous_takes or set()
        moves = _moves or []
        player_pieces, opponent_pieces = self.white_pawns | self.white_kings, self.black_pawns | self.black_kings
        if player == Player.BLACK:
            opponent_pieces, player_pieces = player_pieces, opponent_pieces
        all_pieces       = player_pieces    | opponent_pieces
        x, y = index % 10, index // 10

        directions = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        for dx, dy in directions:
            captured_piece = (y + dy) * 10 + (x + dx)
            destination    = (y + dy * 2) * 10 + (x + dx * 2)
            if not 0 <= y + dy * 2 < 10 or not 0 <= x + dx * 2 < 10:
                continue
            if not captured_piece in previous_takes and (1 << captured_piece) & opponent_pieces and not (1 << destination) & all_pieces:
                previous_takes.add(captured_piece)
                moves.append(Move(player, is_promotion(y + dy * 2, player), 101, destination, [Take(index, bool((self.white_kings | self.black_kings) & (1 << index))) for index in previous_takes]))
                self._get_pawn_takes(player, destination, previous_takes, moves)
                previous_takes.remove(captured_piece)

        for move in moves:
            move.origin = index

        return moves

    def _get_pawn_moves(self, player: Player, index: int) -> list[Move]:
        moves: list[Move] = []
        player_pieces, opponent_pieces = self.white_pawns | self.white_kings, self.black_pawns | self.black_kings
        if player == Player.BLACK:
            opponent_pieces, player_pieces = player_pieces, opponent_pieces
        all_pieces       = player_pieces    | opponent_pieces
        direction = 1 if player == Player.WHITE else -1
        x, y = index % 10, index // 10

        # normal forward moves
        if 0 <= x - 1 < 10 and 0 <= y < 10 and not (1 << ((y + direction) * 10 + x - 1)) & all_pieces:
            move = Move(player, is_promotion(y + direction, player), index, (y + direction) * 10 + x - 1, [])
            moves.append(move)
        if 0 <= x + 1 < 10 and 0 <= y < 10 and not (1 << ((y + direction) * 10 + x + 1)) & all_pieces:
            move = Move(player, is_promotion(y + direction, player), index, (y + direction) * 10 + x + 1, [])
            moves.append(move)

        return moves + self._get_pawn_takes(player, index)

    def _get_pawns_moves(self, player: Player) -> list[Move]:
        board = self.white_pawns if player == Player.WHITE else self.black_pawns
        pieces_moves: list[list[Move]] = []

        for i in range(100):
            if board & (1 << i):
                pieces_moves.append(self._get_pawn_moves(player, i))

        return [move for piece_moves in pieces_moves for move in piece_moves]

    def _get_king_takes(self, player: Player, index: int) -> list[Move]:
        return []

    def _get_king_moves(self, player: Player, index: int) -> list[Move]:
        moves: list[Move] = []
        player_pieces, opponent_pieces = self.white_pawns | self.white_kings, self.black_pawns | self.black_kings
        if player == Player.BLACK:
            opponent_pieces, player_pieces = player_pieces, opponent_pieces
        all_pieces       = player_pieces    | opponent_pieces
        x, y = index % 10, index // 10

        directions = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        for dx, dy in directions:
            for i in range(1, 10):
                cx = x + dx * i
                cy = y + dy * i
                destination = cy * 10 + cx
                if not 0 <= cx < 10 or not 0 <= cy < 10 or all_pieces & (1 << destination):
                    break
                move = Move(player, False, index, destination, [])
                moves.append(move)

        return moves + self._get_king_takes(player, index)

    def _get_kings_moves(self, player: Player) -> list[Move]:
        board = self.white_kings if player == Player.WHITE else self.black_kings
        pieces_moves: list[list[Move]] = []

        for i in range(100):
            if board & (1 << i):
                pieces_moves.append(self._get_king_moves(player, i))

        return [move for piece_moves in pieces_moves for move in piece_moves]

    def get_moves(self) -> list[Move]:
        current_player = self.get_current_player()
        all_moves = self._get_pawns_moves(current_player) + self._get_kings_moves(current_player)
        greatest_take_number = max([len(move.takes) for move in all_moves])
        legal_moves = [move for move in all_moves if len(move.takes) == greatest_take_number]
        return legal_moves

def main():
    board = Checkers()
    board.init_board()
    board.show_board()
    
    for i in range(1000):
        input()
        print(f"-- move {i} --")
        moves = board.get_moves()
        if not moves:
            print("no more move")
            break
        move = random.choice(moves)
        print(move.origin, move.destination)
        board.make_move(move)
        board.show_board()

if __name__ == "__main__":
    main()
