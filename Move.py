from consts import *
from Take import Take

class Move:
    def __init__(self, player: Player, is_promotion: bool, origin: int, destination: int, takes: list[Take]):
        self.player = player
        self.is_promotion = is_promotion
        self.origin = origin
        self.destination = destination
        self.takes = takes
