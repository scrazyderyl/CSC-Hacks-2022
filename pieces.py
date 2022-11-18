from abc import abstractmethod
from pygame.rect import Rect
from graphics import PieceDrawer

piece_drawer = PieceDrawer()

class PieceGroup:
    def __init__(self):
        self.pieces = []
    
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
        # self.group.add(self)

        self.drag_start_x = None
        self.drag_start_y = None

        self.grid_x = None
        self.grid_y = None

    def set_group(self, group):
        self.group = group

    def set_position(self, x, y):
        self.drag_start_x = None
        self.drag_start_y = None
        self.x = x
        self.y = y
        
        self.hitbox = Rect(x + self.hitbox_offset, y + self.hitbox_offset, self.hitbox_size, self.hitbox_size)

    def set_grid_position(self, x, y):
        self.grid_x = x
        self.grid_y = y

    def blit(self, target_surface):
        target_surface.blit(self.surface, (self.x, self.y), target_surface.get_rect())
    
    @abstractmethod
    def contains_point(self, position):
        pass

    def drag(self, dx, dy):
        if self.drag_start_x == None:
            self.drag_start_x = self.x
            self.drag_start_y = self.y

        self.x = self.drag_start_x + dx
        self.y = self.drag_start_y + dy

    def return_pieces(self):
        if self.drag_start_x != None:
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
    def __init__(self, edges):
        super().__init__("cube")

        self.top = None; self.right = None; self.bottom = None; self.left = None

        for side in edges.keys():
            edge = edges[side]
            slot = edge["slot"]
            recessed = edge["recessed"]

            setattr(self, side, Edge(slot, recessed))
        
        self.surface = piece_drawer.draw([self.top, self.right, self.bottom, self.left])
        self.hitbox_size = piece_drawer.hitbox_size
        self.render_size = piece_drawer.render_size
        self.hitbox_offset = piece_drawer.start_offset

    def contains_point(self, position):
        return self.hitbox.collidepoint(position)

    @staticmethod
    def cube_cube_tb_compat(top, bottom):
        if top.bottom == None and bottom.top == None:
            return True
        
        if top.bottom == None and bottom.top != None or top.bottom != None and bottom.top == None:
            return False

        return top.bottom.slot == bottom.top.slot and top.bottom.recessed != bottom.top.recessed

    @staticmethod
    def cube_cube_lr_compat(left, right):
        if left.right == None and right.left == None:
            return True

        if left.right == None and right.left != None or left.right != None and right.left == None:
            return False

        return left.right.slot == right.left.slot and left.right.recessed != right.left.recessed