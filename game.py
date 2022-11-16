import math, json
from pygame import display
from graphics import PieceSurface
from pieces import *

class Player:
    def __init__(self):
        pass

class Level:
    def __init__(self, level_name):
        with open("levels/" + level_name + ".json", "r", encoding="utf-8-sig") as file:
            level_data = json.load(file)

            self.name = level_data["name"]
            self.pieces = level_data["pieces"]
            self.grid_x = level_data["num_columns"]
            self.grid_y = level_data["num_rows"]

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
    
    def redraw(self):
        self.screen.fill((255, 255, 255))
        self.pieces_list.render()
        self.board.render()

        for piece in self.pieces:
            piece.draw()

        display.flip()

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
            self.redraw()

    def on_mouseup(self, event):
        if self.drag_target != None:
            # self.board.on_drop(self.drag_target, event.pos)
            self.drag_target.return_piece()
            self.drag_target = None
            self.redraw()

class Piece_List:
    def __init__(self, parent_surface, pieces):
        self.surface = parent_surface
        self.pieces = pieces
        self.set_positions()

    def set_positions(self):
        y = 40
        y_offset = PieceSurface.SCALE * PieceSurface.BASE_LENGTH + 40

        for piece in self.pieces:
            piece.set_position(40, y)
            y += y_offset
    
    def add_piece(self, piece):
        self.pieces.append(piece)

    def remove_piece(self, piece):
        self.pieces.remove(piece)

    def clear(self):
        self.pieces.clear()

    def render(self):
        pass
        
class Board:
    def __init__(self, parent_surface, pieces, level):
        self.surface = parent_surface.subsurface(parent_surface.get_rect())
        self.x = 300
        self.y = 100
        self.cell_size = PieceSurface.BASE_LENGTH * PieceSurface.SCALE

        self.outline = [OutlinePiece(piece["shape"], piece["grid_x"], piece["grid_y"]) for piece in pieces]
        self.groups = []
        self.level = level
        self.grid = [[] for i in range(level.grid_x)]
        for i in self.grid:
            while(len(i) < level.grid_y):
                i.append(0)

    def new_group(self, piece):
        group = PieceGroup()
        group.add(piece)
        self.groups.append(group)
        return group

    def remove_group(self, group):
        self.groups.remove(group)

    def render(self):
        pass
    
    def calculate_grid_pos(self, position):
        gridx = math.floor((position[0] - self.x) / self.cell_size)
        gridy = math.floor((position[1] - self.y) / self.cell_size)
        return (gridx, gridy)

    def fits_grid(self, target, grid_pos):
        # check fits outline and not overlapping other blocks
        pass

    #The adj_pieces list contains the positions of the already placed 
    # adjacent pieces for the specified grid_pos
    # I know this isn't the most readable code, but I couldn't think of another way 
    #to handle corner and edge pieces that wouldn't cause an index out of bounds error
    # 1 = North, 2 = East, 3 = South, 4 = West
    # matrix is self.grid
    # Returns a list of tuples, each tuple containing the type of adjacency 
    # and the coordinates of an adjacent piece  i.e. (2, x_coord, y_coord)
    def find_adj_pieces(self, grid_pos, matrix):
        adj_pieces = []

        if(grid_pos[0] != 0):
            if(matrix[grid_pos[0]-1][grid_pos[1]] != 0):
                adj_pieces.append(4, matrix[grid_pos[0]-1][grid_pos[1]])
        if(grid_pos[0] != self.level.grid_x):
            if(matrix[grid_pos[0]+1][grid_pos[1]] != 0):
                adj_pieces.append(2, matrix[grid_pos[0]+1][grid_pos[1]] )
        if(grid_pos[1] != 0):
            if(matrix[grid_pos[0]][grid_pos[1]-1] != 0):
                adj_pieces.append(1, matrix[grid_pos[0]][grid_pos[1]-1])
        if(grid_pos[1] != self.level.grid_y):
            if(matrix[grid_pos[0]][grid_pos[1]+1] != 0 ):
                adj_pieces.append(3, matrix[grid_pos[0]][grid_pos[1]+1])

        return adj_pieces


    def get_compatible(self, target, grid_pos):
        # Return true is all adjacent blocks compatible
        # Return false is at least one adjacent block incompatible
        # Return none is there are no adjacent blocks
        #for pieces adjacent to target 
        #check that each adjacent edge is compatible with the respective edge of the t piece
        #if target has piece to the north, check that north edge is 
        #compatible with 
        adj_pieces = self.find_adj_pieces(grid_pos, self.grid)
        if(len(adj_pieces) == 0):
            return None
        for adj_p in adj_pieces:
            if(adj_p[0] == 1 and not cube_cube_tb_compat(adj_p[1], target)):
                return False
            elif(adj_p[0] == 3 and not cube_cube_tb_compat(target, adj_p[1])):
                return False
            elif(adj_p[0] == 4 and not cube_cube_lr_compat(adj_p[1], target)):
                return False
            elif(adj_p[0] == 2 and not cube_cube_lr_compat(target, adj_p[1])):
                return False
        return True
        

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

