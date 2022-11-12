import math
from pygame import rect, sprite

class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score

class Level:
    def __init__(self, level_data):
        self.name = level_data.name
        self.shapes = level_data.shapes
        self.outline = level_data.outline

class Board:
    def __init__(self, outline):
        self.outline = outline

    def add_to_group(self, piece):
        pass

    def add_piece(self, piece):
        self.placed_pieces.append(piece)

    def remove_piece(self, piece):
        self.placed_pieces.remove(piece)

class Edge:
    def __init__(self, slot, recessed):
        self.slot = slot
        self.recessed = recessed

class Object:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y

class Cube(Object):
    def __init__(self, edges, selected):
        super("cube")
        self.top = edges[0]
        self.right = edges[1]
        self.bottom = edges[2]
        self.left = edges[3]
        self.selected = selected

    @staticmethod
    def cube_cube_tb_compat(top, bottom):
        return top.bottom.slot == bottom.top.slot and top.bottom.recessed != bottom.bottom.recessed

    @staticmethod
    def cube_cube_lr(left, right):
        return left.bottom.slot == right.top.slot and left.bottom.recessed != right.bottom.recessed

