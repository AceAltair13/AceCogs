'''
A Small Minigame where main objective is to collect coins in limited number of moves
[@] : Player
[·] : Visited
[○] : Coin
[+] : Power-Ups
[R] : Reveal-Shard
'''

import random
from enum import Enum
from textwrap import dedent


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

    def show_symbol(self):
        if self.visible:
            if self.has == Pickup.coin:
                return '○'
            elif self.has == Pickup.power:
                return '+'
            elif self.has == Pickup.reveal:
                return 'R'
            elif self.has == Pickup.empty:
                return '.'
        else:
            return ' '


class CoinGame:

    def reveal_near(self):
        x, y = self.player
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if not (dx or dy):
                    continue
                cell = self.coinmap.get((x + dx, y + dy))
                if cell is not None:
                    cell.reveal()

    def __init__(self):

        self.stats = {
            'coins': 0,
            'power': 0,
            'reveal': 0,
            'max_coins': 0,
            'max_power': 0,
            'max_reveal': 0,
            'moves': 25,
            'max_moves': 25
        }
        self.player = (8, 4)
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

        self.stats['max_coins'] = put_stuff(self, Pickup['coin'], 30, 35)
        self.stats['max_power'] = put_stuff(self, Pickup['power'], 5, 10)
        self.stats['max_reveal'] = put_stuff(self, Pickup['reveal'], 0, 1)
        self.reveal_near()

    def move_player(self, dir):
        # | 0: right | 1: up | 2: left | 3: down |
        x, y = self.player
        if dir == Direction.right:
            if not y == 8:
                y += 1
        elif dir == Direction.down:
            if not x == 8:
                x += 1
        elif dir == Direction.left:
            if not y == 0:
                y -= 1
        elif dir == Direction.up:
            if not x == 0:
                x -= 1
        self.player = (x, y)
        item_ = self.coinmap[(x, y)].collect()
        if item_ == Pickup.coin:
            self.stats["coins"] += 1
        elif item_ == Pickup.power:
            self.stats["power"] += 1
            self.stats['max_moves'] += 5
            self.stats['moves'] += 6
        elif item_ == Pickup.reveal:
            self.stats["reveal"] += 1
            for cell in self.coinmap.values():
                cell.reveal()
        self.coinmap[(x, y)].reveal()
        self.stats['moves'] -= 1
        self.reveal_near()

    def render(self):
        symbols = []
        for i in range(9):
            for j in range(9):
                if not (i, j) == self.player:
                    symbols.append(self.coinmap[(i, j)].show_symbol())
                else:
                    symbols.append('@')

        return dedent("""
        #####################
        # {} {} {} {} {} {} {} {} {} #
        # {} {} {} {} {} {} {} {} {} #
        # {} {} {} {} {} {} {} {} {} #
        # {} {} {} {} {} {} {} {} {} #
        # {} {} {} {} {} {} {} {} {} #
        # {} {} {} {} {} {} {} {} {} #
        # {} {} {} {} {} {} {} {} {} #
        # {} {} {} {} {} {} {} {} {} #
        # {} {} {} {} {} {} {} {} {} #
        #####################
        Moves: {}
        Coins: {} / {}
        Power-Ups: {} / {}
        Reveals: {} / {}
        """.format(
            *symbols, self.stats['moves'],
            self.stats['coins'], self.stats['max_coins'], self.stats['power'],
            self.stats['max_power'], self.stats['reveal'], self.stats['max_reveal']
        ))
