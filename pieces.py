from abc import abstractmethod
from pygame import rect
from graphics import PieceSurface

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
        self.drag_start_x = None
        self.drag_start_y = None

    def set_group(self, group):
        self.group = group
    
    def remove_group(self):
        self.group = None

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect = rect.Rect(x, y, self.surface.size, self.surface.size)

    def draw(self):
        self.surface.render(self.x, self.y)
    
    @abstractmethod
    def contains_point(self, position):
        pass

    def drag(self, dx, dy):
        if self.drag_start_x == None:
            self.drag_start_x = self.x
            self.drag_start_y = self.y

        self.x = self.drag_start_x + dx
        self.y = self.drag_start_y + dy

    def return_piece(self):
        self.x = self.drag_start_x
        self.y = self.drag_start_y
        self.drag_start_x = None
        self.drag_start_y = None

class OutlinePiece:
    def __init__(self, shape, grid_x, grid_y):
        self.shape = shape
        self.grid_x = grid_x
        self.grid_y = grid_y

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