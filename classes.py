import math, json
from abc import abstractmethod
from pygame import rect

class Player:
    def __init__(self):
        pass

class Level:
    def __init__(self, level_name):
        with open("levels/" + level_name + ".json", "r", encoding="utf-8-sig") as file:
            level_data = json.load(file)

            self.name = level_data.name
            self.shapes = level_data.shapes
            self.outline = level_data.outline

class Game:
    def __init__(self):
        pass

    def load_level(self, level_name):
        self.player = None

        level = Level(level_name)
        self.pieces_list = Piece_List(level.pieces)
        self.board = Board(level.outline)
        self.dragTarget = None

    def on_mousedown(self, position):
        clicked = self.pieces_list.get_clicked(position)

        if clicked != None:
            self.dragTarget = clicked

        clicked = self.board.get_clicked(position)

        if clicked != None:
            self.dragTarget = clicked

    def on_mousemove(self, position):
        if self.dragTarget != None:
            self.board.drag(self.dragTarget, position)

    def on_mouseup(self, position):
        self.board.drop(self.dragTarget, position)

        self.dragTarget = None

class Piece_List:
    def __init__(self, pieces, xpos, ypos):
        self.pieces = pieces
        self.xpos = xpos
        self.ypos = ypos
    
    def add_piece(self, piece):
        self.pieces.append(piece)

    def remove_piece(self, piece):
        self.pieces.remove(piece)

    def clear(self):
        self.pieces.clear()

    def get_clicked(self, position):
        for piece in self.pieces:
            if piece.contains_point(position):
                return piece
        
        return None

class Board:
    def __init__(self, outline, xpos, ypos, cell_size):
        self.outline = outline
        self.groups = []

        self.xpos = xpos
        self.ypos = ypos
        self.cell_size = cell_size

    def new_group(self, piece):
        group = PieceGroup(piece)
        self.groups.append(group)

    def add_to_group(self, piece):
        for group in self.groups:
            if (group.can_accept(piece)):
                group.add(piece)
                return
        
        self.new_group(piece)
    
    def get_clicked(self, position, mouse_state):
        for group in self.groups:
            piece = group.check_clicked(position)

            if group.check_clicked(position):
                # left click
                if mouse_state[0]:
                    return group
                # right click
                elif mouse_state[1]:
                    return piece
        
        return None
    
    def get_grid_position(self, position):
        gridx = math.floor((position[0] - self.xpos) / self.cell_size)
        gridy = math.floor((position[1] - self.ypos) / self.cell_size)
        return (gridx, gridy)

    def get_compatible(self, target, grid_pos):
        if type(target) == "PieceGroup":
            compatible = [group for group in self.groups if group.can_accept_group(target, grid_pos)]
        elif type(target) == "Piece":
            compatible = [group for group in self.groups if group.can_accept_piece(target, grid_pos)]
                
        if len(compatible) == 0:
            return None
        else:
            return compatible

    def is_empty_and_not_adjacent(self, target, grid_pos):
        if type(target) == "PieceGroup":
            pass
        elif type(target) == "Piece":
            pass

    def drag(self, target, position):
        grid_pos = self.get_grid_position(position)
        group = self.get_compatible(target, grid_pos)

        if group != None or self.is_empty_and_not_adjcent(grid_pos):
            pass
    
    def drop(self, target, position):
        grid_pos = self.get_grid_position(position)
        group = self.get_compatible(target, grid_pos)

        if group != None:
            group.add(target)
            target.drop(grid_pos)
        elif self.is_empty_and_not_adjcent(grid_pos):
            self.new_group(target)
            target.drop(grid_pos)
        else:
            target.return_pieces()

class PieceGroup:
    def __init__(self, piece):
        self.pieces = [piece]
    
    def add(self, piece):
        if type(piece) == "PieceGroup":
            self.merge(piece)
        elif type(piece) == "Piece":
            self.pieces.append(piece)
            piece.set_group(self)
    
    def remove(self, piece):
        self.pieces.remove(piece)

    def merge(self, group):
        for piece in group.pieces:
            self.add(piece)
            self.set_group(self)

    def check_clicked(self, position):
        for piece in self.pieces:
            if piece.contains_point(position):
                return piece
        
        return False

    def can_accept_group(self, group, grid_pos):
        pass

    def can_accept_piece(self, piece, grid_pos):
        pass

    def drag(self, position):
        for piece in self.pieces:
            pass
    
    def drop(self, grid_pos):
        for piece in self.pieces:
            pass

    def return_pieces(self):
        for piece in self.pieces:
            piece.return_piece()

class Piece:
    def __init__(self, type, xpos, ypos, size):
        self.type = type
        self.group = None

        self.gridx = None
        self.gridy = None

        self.xpos = xpos
        self.ypos = ypos
        self.size = size

    def set_pos(self, x, y):
        self.xpos = x
        self.ypos = y

    def set_group(self, group):
        self.group = group
    
    def remove_group(self):
        self.group = None
    
    @abstractmethod
    def contains_point(self, position):
        pass

    def drag(self, position):
        # render
        pass

    def drop(self, grid_pos):
        self.gridx = grid_pos[0]
        self.gridy = grid_pos[1]

        # render

    def return_piece(self):
        # render
        pass

class Edge:
    def __init__(self, slot, recessed):
        self.slot = slot
        self.recessed = recessed

class Cube(Piece):
    def __init__(self, xpos, ypos, size, edges):
        super.__init__("cube", xpos, ypos, size)
        self.rect = rect(xpos, ypos, size, size)

        self.top = edges[0]
        self.right = edges[1]
        self.bottom = edges[2]
        self.left = edges[3]
    
    def contains_point(self, position):
        return self.rect.contains(position)

    @staticmethod
    def cube_cube_tb_compat(top, bottom):
        return top.bottom.slot == bottom.top.slot and top.bottom.recessed != bottom.bottom.recessed

    @staticmethod
    def cube_cube_lr_compat(left, right):
        return left.right.slot == right.left.slot and left.right.recessed != right.left.recessed

