import math, json
from abc import abstractmethod
from graphics import PieceSurface
from pygame import display, rect

class Player:
    def __init__(self):
        pass

class Level:
    def __init__(self, level_name):
        with open("levels/" + level_name + ".json", "r", encoding="utf-8-sig") as file:
            level_data = json.load(file)

            self.name = level_data["name"]
            self.pieces = level_data["pieces"]

class Game:
    def __init__(self, screen):
        self.screen = screen

    def load_level(self, level_name):
        self.player = None

        level = Level(level_name)
        self.pieces = [Cube(self.screen, piece["edges"]) for piece in level.pieces]
        self.pieces_list = Piece_List(self.screen, self.pieces.copy())
        self.board = Board(self.screen, level.pieces)
        self.drag_target = None
    
    def start_level(self):
        self.pieces_list.render()
        self.board.render()

    def on_mousedown(self, event):
        if event.button == 1 or event.button == 3:
            for piece in self.pieces:
                if piece.contains_point(event.pos):
                    self.drag_start_x = event.pos[0]
                    self.drag_start_y = event.pos[1]

                    if event.button == 1 and piece.group != None:
                        self.drag_target = piece.group
                    else:
                        self.drag_target = piece
                    
                    break

    def on_mousemove(self, event):
        if self.drag_target != None:
            dx = event.pos[0] - self.drag_start_x
            dy = event.pos[1] - self.drag_start_y

            self.drag_target.drag(dx, dy)
            self.board.on_drag(self.drag_target, event.pos)

    def on_mouseup(self, event):
        if self.drag_target != None:
            self.board.on_drop(self.drag_target, event.pos)
            self.drag_target = None

class Piece_List:
    def __init__(self, parent_surface, pieces):
        self.surface = parent_surface
        self.pieces = pieces
    
    def add_piece(self, piece):
        self.pieces.append(piece)

    def remove_piece(self, piece):
        self.pieces.remove(piece)

    def clear(self):
        self.pieces.clear()

    def render(self):
        y = 40
        y_offset = PieceSurface.SCALE * PieceSurface.BASE_LENGTH + 40

        for piece in self.pieces:
            piece.set_position(40, y)
            y += y_offset

        display.update(self.surface.get_rect())

class Board:
    def __init__(self, parent_surface, pieces):
        self.surface = parent_surface.subsurface(parent_surface.get_rect())
        self.x = 300
        self.y = 100
        self.cell_size = PieceSurface.BASE_LENGTH * PieceSurface.SCALE

        self.outline = [OutlinePiece(piece["shape"], piece["grid_x"], piece["grid_y"]) for piece in pieces]
        self.groups = []

    def new_group(self, piece):
        group = PieceGroup()
        group.add(piece)
        self.groups.append(group)
        return group

    def remove_group(self, group):
        self.groups.remove(group)

    def render(self):
        display.update(self.surface.get_rect())
    
    def calculate_grid_pos(self, position):
        gridx = math.floor((position[0] - self.x) / self.cell_size)
        gridy = math.floor((position[1] - self.y) / self.cell_size)
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
            
    def on_drop(self, target, position):
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

    def drag(self, dx, dy):
        for piece in self.pieces:
            piece.drag(dx, dy)

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

    def set_group(self, group):
        self.group = group
    
    def remove_group(self):
        self.group = None

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect = rect.Rect(x, y, self.surface.size, self.surface.size)
        self.draw(x, y)

    def draw(self, x, y):
        self.surface.render(x, y)
    
    @abstractmethod
    def contains_point(self, position):
        pass

    def drag(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        self.draw(new_x, new_y)

    def return_piece(self):
        self.draw(self.x, self.y)

class OutlinePiece:
    def __init__(self, shape, gridx, gridy):
        self.shape = shape
        self.grid_x = gridx
        self.grid_y = gridy

class Cube(Piece):
    def __init__(self, surface, edges):
        super().__init__("cube")

        self.top = None; self.right = None; self.bottom = None; self.left = None

        for side in edges.keys():
            edge = edges[side]
            slot = edge["slot"]
            recessed = edge["recessed"]

            setattr(self, side, Edge(slot, recessed))
        
        self.surface = PieceSurface(surface, [self.top, self.right, self.bottom, self.left])

    def contains_point(self, position):
        return self.rect.collidepoint(position)

    @staticmethod
    def cube_cube_tb_compat(top, bottom):
        return top.bottom.slot == bottom.top.slot and top.bottom.recessed != bottom.bottom.recessed

    @staticmethod
    def cube_cube_lr_compat(left, right):
        return left.right.slot == right.left.slot and left.right.recessed != right.left.recessed

