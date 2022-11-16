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
            self.grid_x = level_data["grid_x"]
            self.grid_y = level_data["grid_y"]

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
    def __init__(self, parent_surface, pieces):
        self.surface = parent_surface.subsurface(parent_surface.get_rect())
        self.x = 300
        self.y = 100
        self.cell_size = PieceSurface.BASE_LENGTH * PieceSurface.SCALE

        self.outline = [OutlinePiece(piece["shape"], piece["grid_x"], piece["grid_y"]) for piece in pieces]
        self.groups = []
        # self.grid = [0]*level.grid_x
        # for i in self.grid:
        #     i = [0]*level.grid_y

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

    #The adj_blocks list contains the number and type of adjacent blocks for the specified grid_pos
    # 1 = north, 2 = east, 3 = south, 4 = west
    # Returns a list of tuples, each tuple being the coordinates of an adjacent block
    def find_adj_blocks(grid_pos):
        adj_blocks = [1, 2, 3, 4]
        # if(grid_pos[0] == 0):
        #     adj_blocks.remove(4)
        # if(grid_pos[0] == outlinepiece.grid_x):
        #     adj_blocks.remove(2)
        # if(grid_pos[1] == 0):
        #     adj_blocks.remove(3)
        # if(grid_pos[1] == outlinepiece.grid_y):
        #     adj_blocks.remove(1)
        
        adj_b_pos = []
        for b in adj_blocks:
            if(b == 1):
                adj_b_pos.append((grid_pos[0], grid_pos[1]-1))
            if(b == 2):
                adj_b_pos.append((grid_pos[0]+1, grid_pos[1]))
            if(b == 3):
                adj_b_pos.append((grid_pos[0], grid_pos[1]+1))
            if(b == 4):
                adj_b_pos.append((grid_pos[0]-1, grid_pos[1]))
        return adj_b_pos


    def get_compatible(self, target, grid_pos):
        # Return true is all adjacent blocks compatible
        # Return false is at least one adjacent block incompatible
        # Return none is there are no adjacent blocks
        #for pieces adjacent to target 
        #check that each adjacent edge is compatible with the respective edge of the t piece
        #if target has piece to the north, check that north edge is 
        #compatible with 
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

