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

map = {}


class Cell:
    def __init__(self, type):
        pass


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


def make_map():
    for i in range(9):
        for j in range(9):
            map[(i, j)] = Place().put_elements()
    map[(5, 5)] = None
    print(map)
    coins = power = reveal = 0
    for val in map.values():
        if val == 'coin':
            coins += 1
        elif val == 'power':
            power += 1
        elif val == 'special':
            reveal += 1
    print(f"Coins: {coins}\nPower-Ups: {power}\nReveals: {reveal}")


class Place:
    @staticmethod
    def put_elements():
        if random.random() < 0.7:
            chance = random.random()
            if chance <= (2 / 99):
                return 'special'
            elif chance > (2 / 99) and chance < (20 / 99):
                return 'power'
            else:
                return 'coin'
        else:
            return


make_map()
