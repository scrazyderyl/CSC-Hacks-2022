import math, json
import random
from pygame import display
from graphics import PieceDrawer
from pieces import *
import pygame

class Player:
    def __init__(self):
        pass

class Level:
    def __init__(self, level_name):
        with open("levels/" + level_name + ".json", "r", encoding="utf-8-sig") as file:
            level_data = json.load(file)

            self.name = level_data["name"]
            self.pieces = level_data["pieces"]
            self.num_columns = level_data["num_columns"]
            self.num_rows = level_data["num_rows"]

class Game:
    def __init__(self, screen):
        self.screen = screen

    def load_level(self, level_name):
        self.player = None

        level = Level(level_name)
        self.pieces = [Cube(piece["edges"]) for piece in level.pieces]
        self.pieces_list = Piece_List(self.screen, self.pieces.copy())
        self.board = Board(self.screen, self.pieces.copy(), level)
        self.drag_target = None
    
    def redraw(self):
        self.screen.fill((255, 255, 255))
        self.pieces_list.render()
        self.board.render()

        for piece in self.pieces:
            piece.blit(self.screen)

        display.flip()

    def on_mousedown(self, event):
        if event.button == 1 or event.button == 3:
            self.drag_as_group = event.button == 1

            for piece in self.pieces:
                if piece.contains_point(event.pos):
                    self.drag_start_x, self.drag_start_y = event.pos
                    self.drag_target = piece
                    break

    def on_mousemove(self, event):
        if self.drag_target != None:
            x, y = event.pos
            dx = x - self.drag_start_x
            dy = y - self.drag_start_y

            self.drag_target.drag(dx, dy)
            self.redraw()

    def on_mouseup(self, event):
        if self.drag_target != None:
            self.board.on_drop(self.drag_target, event.pos, self.drag_as_group)
            self.drag_target = None
            self.redraw()

class Piece_List:
    def __init__(self, parent_surface, pieces):
        self.surface = parent_surface
        self.pieces = pieces
        self.set_positions()

    def set_positions(self):
        y = 500
        x = 0

        for piece in self.pieces:
            if x < 700:
                x += piece.render_size + 50
            else:
                y += piece.render_size +50
            
            piece.set_position(x, y)
    
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
        self.cell_size = PieceDrawer.BASE_LENGTH * PieceDrawer.SCALE

        self.pieces = pieces
        self.groups = []

        self.level = level
        self.grid = [[None]*level.num_rows for i in range(level.num_columns)]
        self.board_style = random.randint(1, 6)

    def new_group(self, piece):
        group = PieceGroup()
        group.add(piece)
        self.groups.append(group)
        return group

    def remove_group(self, group):
        self.groups.remove(group)

    def set_pos(self, piece, grid_pos):
        grid_x, grid_y = grid_pos
        piece.grid_x = grid_x
        piece.grid_y = grid_y
        x = self.x + self.cell_size * grid_x - piece.hitbox_offset
        y = self.y + self.cell_size * grid_y - piece.hitbox_offset
        piece.set_position(x, y)

    def render(self):
        width = self.cell_size * self.level.num_columns
        height = self.cell_size * self.level.num_rows
        rect = Rect(self.x, self.y, width, height)
        pygame.draw.rect(self.surface, (230, 230, 230), rect)

        # if board == 1:
        #     pygame.draw.rect(self.surface, (169, 205, 238), grid1)
        # elif board == 2:
        #     pygame.draw.circle(self.surface, (0, 205, 238), (375, 320), 250)
        # elif board == 3:
        #     pygame.draw.polygon(self.surface, (155, 0, 155), [(100, 300), (300, 500), (600, 300), (300, 300), (200, 50)])
        # elif board == 4:
        #     pygame.draw.polygon(self.surface, (0, 0, 155), [(120,100),(550,500),(250,500)])
        # elif board == 5:
        #     pygame.draw.polygon(self.surface, (0, 155, 155), [(100, 103), (600, 101), (415, 486), (385, 288)])
        # elif board == 6:
        #     pygame.draw.polygon(self.surface, (255,255,153), [(265, 151), (300, 20), (335, 151), (471, 144), (357, 219), (406, 346), (300, 260), (194, 346), (243, 219), (129, 144)])
    
    def calculate_grid_pos(self, position):
        x, y = position
        grid_x = math.floor((x - self.x) / self.cell_size)
        grid_y = math.floor((y - self.y) / self.cell_size)
        return (grid_x, grid_y)

    def is_position_valid(self, grid_pos):
        grid_x, grid_y = grid_pos
        return grid_x >= 0 and grid_y >= 0 and grid_x < self.level.num_columns and grid_y < self.level.num_rows and self.grid[grid_x][grid_y] == None

    def fits_grid(self, target, grid_pos, drag_as_group):
        grid_x, grid_y = grid_pos

        # Handle piece not on grid
        if target.grid_x == None or target.group == None:
            return self.is_position_valid(grid_pos)

        dx = grid_x - target.grid_x
        dy = grid_y - target.grid_y

        # check if each piece in group is valid
        if drag_as_group:
            for piece in target.group:
                new_x = piece.grid_x + dx
                new_y = piece.grid_y + dy

                if not self.is_position_valid((new_x, new_y)):
                    return False
        else:
        # drag as individual piece
            if not self.is_position_valid((new_x, new_y)):
                return False

        return True
    
    def is_piece_compatible(self, excluded_pieces, piece, grid_pos):
        grid_x, grid_y = grid_pos

        # check top
        if grid_y - 1 >= 0:
            top_piece = self.grid[grid_x][grid_y - 1]
            bottom_piece = piece

            if top_piece != None and top_piece not in excluded_pieces and not Cube.cube_cube_tb_compat(top_piece, piece):
                return False

        # check bottom
        if grid_y + 1 <= self.level.num_rows - 1:
            top_piece = piece
            bottom_piece = self.grid[grid_x][grid_y + 1]

            if bottom_piece != None and bottom_piece not in excluded_pieces and not Cube.cube_cube_tb_compat(top_piece, bottom_piece):
                return False

        # check left
        if grid_x - 1 >= 0:
            left_piece = self.grid[grid_x - 1][grid_y]
            right_piece = piece

            if left_piece != None and left_piece not in excluded_pieces and not Cube.cube_cube_lr_compat(left_piece, right_piece):
                return False
                
        # check right
        if grid_x + 1 <= self.level.num_columns - 1:
            left_piece = piece
            right_piece = self.grid[grid_x + 1][grid_y]

            if right_piece != None and right_piece not in excluded_pieces and not Cube.cube_cube_lr_compat(left_piece, right_piece):
                return False
        
        return True

    def is_group_compatible(self, target, grid_pos, drag_as_group):
        if drag_as_group:
            grid_x, grid_y = grid_pos

            if grid_x == None:
                dx = grid_x - target.grid_x
                dy = grid_y - target.grid_y

                for piece in target.group.pieces:
                    new_x = piece.grid_x + dx
                    new_y = piece.grid_y + dy

                    if not self.is_piece_compatible(target.group.pieces, piece, (new_x, new_y)):
                        return False
            else:
                dx = 0
                dy = 0

                if not self.is_piece_compatible(target, target, grid_pos):
                    return False
        else:
            if not self.is_piece_compatible(target.group.pieces, target, grid_pos):
                return False
        
        return True
            
    def on_drop(self, target, position, drag_as_group):
        grid_pos = self.calculate_grid_pos(position)
        grid_x, grid_y = grid_pos

        if self.fits_grid(target, grid_pos, drag_as_group):
            if target.group == None:
                compatible = self.is_piece_compatible([], target, grid_pos)
            else:
                compatible = self.is_group_compatible(target, grid_pos, drag_as_group)

            # droppable, not adjacent to other blocks
            if compatible == True:
                if target.grid_x != None:
                    self.grid[target.grid_x][target.grid_y] = None

                self.grid[grid_x][grid_y] = target
                self.set_pos(target, grid_pos)
            else:
                target.return_pieces()
        else:
            target.return_pieces()

