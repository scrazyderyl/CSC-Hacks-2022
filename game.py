import json
from classes import *

def start_level(level_name):
    pass

def load_level(filename):
    with open(filename, "r", encoding="utf-8-sig"):
        level = json.load(filename)

        return Level(level)

def check_click(position, cubes):
    for cube in cubes:
        if cube.collidepoint(position):
            pass