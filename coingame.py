'''
A Small Minigame where main objective is to collect coins in limited number of moves
[] : Player
[] : Visited
[] : Coin
[] : Power-Ups
[] : Reveal-Shard
'''

import msvcrt
import random
from enum import Enum


class Direction(Enum):
    right = 0
    up = 1
    left = 2
    down = 3


class Pickup(Enum):
    empty = 0
    coin = 1
    power = 2
    reveal = 3


KEYS = {
    'w': Direction.up,
    'a': Direction.left,
    's': Direction.down,
    'd': Direction.right
}


class Cell:
    def __init__(self):
        self.has = Pickup["empty"]
        self.visible = False

    def reveal(self):
        self.visible = True

    def collect(self):
        ret = self.has
        self.has = Pickup["empty"]
        return ret

    def set_pickup(self, has):
        self.has = has

    def is_empty(self):
        return self.has == Pickup["empty"]


class CoinGame:

    def __init__(self):

        self.stats = {
            'coins': 0,
            'power': 0,
            'reveal': 0,
            'max_coins': 0,
            'max_power': 0,
            'max_reveal': 0,
            'moves': 25
        }
        self.player = (5, 0)
        self.coinmap = {}

        for i in range(9):
            for j in range(9):
                self.coinmap[(i, j)] = Cell()
        empty_cells = list(self.coinmap.values())
        empty_cells.remove(self.coinmap[self.player])

        def put_stuff(self, item, wt1, wt2):
            qty = random.randint(wt1, wt2)
            for i in range(qty):
                cell = random.choice(empty_cells)
                empty_cells.remove(cell)
                cell.set_pickup(item)
            return qty

        self.stats['max_coins'] = put_stuff(self, Pickup['coin'], 35, 45)
        self.stats['max_power'] = put_stuff(self, Pickup['power'], 10, 15)
        self.stats['max_reveal'] = put_stuff(self, Pickup['reveal'], 0, 1)

    def move_player(self, dir):
        # | 0: right | 1: up | 2: left | 3: down |
        x, y = self.player
        if dir == 0:
            if not x == 8:
                x += 1
        elif dir == 1:
            if not y == 8:
                y += 1
        elif dir == 2:
            if not x == 0:
                x -= 1
        elif dir == 3:
            if not y == 0:
                y -= 1
        self.player = (x, y)
        item_ = self.coinmap[(x, y)].collect()
        if item_ == Pickup.coin:
            self.stats["coins"] += 1
        elif item_ == Pickup.power:
            self.stats["power"] += 1
        elif item_ == Pickup.reveal:
            self.stats["reveal"] += 1
        self.coinmap[(x, y)].reveal()
        self.stats['moves'] -= 1


def get_key(check, *, print_keys=False):
    while True:
        key = msvcrt.getch().decode()
        if print_keys:
            print(key, end='')
        result = check(key)
        if result is not None:
            return result


def check(key):
    return KEYS.get(key)


game = CoinGame()

while True:
    way = get_key(check)
    game.move_player(way)