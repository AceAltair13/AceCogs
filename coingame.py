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


class Cell:
    def __init__(self):
        self.has = Pickup["empty"]
        self.visible = False

    def reveal(self):
        self.visible = True

    def collect(self):
        self.has = Pickup["empty"]

    def set_pickup(self, has):
        self.has = has

    def is_empty(self):
        return self.has == Pickup["empty"]


class Pickup(Enum):
    empty = 0
    coin = 1
    power = 2
    reveal = 3


class CoinGame:
    def __init__(self):
        self.map = {}
        for i in range(9):
            for j in range(9):
                self.map[(i, j)] = Cell()

        def put_stuff(self, item, wt1, wt2):
            self.qty = random.randint(self.wt1, self.wt2)
            while self.qty:
                self.x, self.y = random.randint(0, 8), random.randint(0, 8)
                if self.map[(self.x, self.y)].is_empty():
                    if self.x != 5 and self.y != 0:
                        self.map[(self.x, self.y)].set_pickup(item)
                        self.qty -= 1
        put_stuff(self, Pickup['coin'], 35, 45)
        put_stuff(self, Pickup['power'], 10, 15)
        put_stuff(self, Pickup['reveal'], 0, 1)


def get_key(check, *, print_keys=False):
    while True:
        key = msvcrt.getch().decode()
        if print_keys:
            print(key, end='')
        result = check(key)
        if result is not None:
            return result


KEYS = ('w', 'a', 's', 'd')


def key_check(key):
    if key in KEYS:
        return key
    return None
