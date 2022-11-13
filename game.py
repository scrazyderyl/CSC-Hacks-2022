import math, json
from abc import abstractmethod

class Player:
    def __init__(self):
        pass

class Level:
    def __init__(self, level_name):
        with open("levels/" + level_name + ".json", "r", encoding="utf-8-sig") as file:
            level_data = json.load(file)

            self.name = level_data.name
            self.pieces = level_data.pieces
            self.outline = level_data.outline

class Game:
    def __init__(self):
        pass

    def load_level(self, level_name):
        self.player = None

        level = Level(level_name)
        self.pieces_list = Piece_List(level.pieces)
        self.board = Board(level.outline)
        self.drag_target = None

    def on_mousedown(self, position):
        clicked = self.pieces_list.get_clicked(position)

        if clicked != None:
            self.drag_target = clicked

        clicked = self.board.get_clicked(position)

        if clicked != None:
            self.drag_target = clicked

    def on_mousemove(self, position):
        if self.drag_target != None:
            self.board.on_drag(self.drag_target, position)

    def on_mouseup(self, position):
        if self.drag_target != None:
            self.board.drop(self.drag_target, position)
            self.drag_target = None

class Piece_List:
    def __init__(self, pieces):
        self.pieces = [getattr(globals, piece["shape"])(piece["edges"]) for piece in pieces]
    
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
    def __init__(self, outline):        
        self.outline = [OutlinePiece(piece["shape"], piece["grid_x"], piece["gridy"]) for piece in outline]
        self.groups = []

    def new_group(self, piece):
        group = PieceGroup()
        group.add(piece)
        self.groups.append(group)
        return group

    def remove_group(self, group):
        self.groups.remove(group)
    
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
    
    def calculate_grid_pos(self, position):
        gridx = math.floor((position[0] - self.xpos) / self.cell_size)
        gridy = math.floor((position[1] - self.ypos) / self.cell_size)
        return (gridx, gridy)

    def fits_grid(self, target, grid_pos):
        # check fits outline and not overlapping other blocks
        pass

    def get_compatible(self, target, grid_pos):
        # Return true is all adjacent blocks compatible
        # Return false is at least one adjacent block incompatible
        # Return none is there are no adjacent blocks
        pass

    def on_drag(self, target, position):
        grid_pos = self.calculate_grid_pos(position)

        if self.fits_grid(target, grid_pos):
            groups = self.get_compatible(target, grid_pos)

            # droppable, not adjacent to other blocks
            if groups == None:
                pass
            # droppable, adjacent to other blocks
            elif groups:
                pass
            
    def drop(self, target, position):
        grid_pos = self.calculate_grid_pos(position)

        if self.fits_grid(target, grid_pos):
            groups = self.get_compatible(target, grid_pos)

            # droppable, not adjacent to other blocks
            if groups == None:
                pass
            # droppable, adjacent to other blocks
            elif groups:
                pass
            # not droppable
            else:
                target.return_pieces()

class PieceGroup:
    def __init__(self):
        self.pieces = []

    def __init__(self, group):
        self.pieces = group.pieces
    
    def add(self, piece):
        self.pieces.append(piece)
        piece.set_group(self)
    
    def merge(self, group):
        for piece in group.pieces:
            self.add(piece)
            
    def remove(self, piece):
        self.pieces.remove(piece)

    def check_clicked(self, position):
        for piece in self.pieces:
            if piece.contains_point(position):
                return piece
        
        return False

    def drag(self, position):
        for piece in self.pieces:
            pass
    
    def drop(self, grid_pos):
        for piece in self.pieces:
            pass

    def return_pieces(self):
        for piece in self.pieces:
            piece.return_piece()

class Edge:
    def __init__(self, slot, recessed):
        self.slot = slot
        self.recessed = recessed

class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.group = None

        self.grid_x = None
        self.grid_y = None

    def set_grid_pos(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y

    def set_group(self, group):
        self.group = group
    
    def remove_group(self):
        self.group = None
    
    @abstractmethod
    def contains_point(self, position):
        pass

    def drag(self, position):
        pass

    def drop(self, grid_pos):
        self.set_grid_pos(grid_pos[0], grid_pos[1])

    def return_piece(self):
        pass

class OutlinePiece:
    def __init__(self, shape, gridx, gridy):
        self.shape = shape
        self.grid_x = gridx
        self.grid_y = gridy

class Cube(Piece):
    def __init__(self, edges):
        super.__init__("cube")

        self.top = None; self.right = None; self.bottom = None; self.left = None

        for side in edges.keys():
            edge = edges[side]
            slot = edge["slot"]
            recessed = edge["recessed"]

            setattr(self, side, Edge(slot, recessed))
    
    def contains_point(self, position):
        return self.rect.contains(position)

    @staticmethod
    def cube_cube_tb_compat(top, bottom):
        return top.bottom.slot == bottom.top.slot and top.bottom.recessed != bottom.bottom.recessed

    @staticmethod
    def cube_cube_lr_compat(left, right):
        return left.right.slot == right.left.slot and left.right.recessed != right.left.recessed

