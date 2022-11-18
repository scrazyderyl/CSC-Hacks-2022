import math
from pygame import Vector2, draw
from pygame.rect import Rect
from pygame.surface import Surface

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class PieceDrawer:
    BASE_LENGTH = 10
    BASE_RADIUS = 2
    SCALE = 6
    BORDER_WIDTH = 2

    square = [(4, 0), (4, 2), (6, 2), (6, 0)]
    rectangle = [(3, 0), (3, 2), (7, 2), (7, 0)]
    triangle = [(4, 0), (5, 2), (6, 0)]
    triangle2 = [(4, 0), (4, 2), (5, 0), (6, 2), (6, 0)]
    semicircle = [(5, 0)]

    def __init__(self):
        self.shapes = {}

        self.fill_color = (255, 0, 255, 255)
        self.border_color = BLACK
        self.set_scale(PieceDrawer.SCALE)

    def set_fill_color(self, color):
        self.fill_color = color

    def set_border_color(self, color):
        self.border_color = color

    def set_scale(self, scale):
        self.scale = scale
        self.edge_length = scale * PieceDrawer.BASE_LENGTH
        self.hitbox_size = scale * PieceDrawer.BASE_LENGTH + math.floor(PieceDrawer.BORDER_WIDTH / 2) + 1
        self.render_size = scale * (PieceDrawer.BASE_LENGTH + 2 * 2) + 4 * math.floor(PieceDrawer.BORDER_WIDTH / 2)
        self.start_offset = scale * 2 + PieceDrawer.BORDER_WIDTH

        for angle in [0, 90, 180, 270]:
            self.shapes[angle] = {
                "square": self.transform_points(PieceDrawer.square, scale, angle),
                "rectangle": self.transform_points(PieceDrawer.rectangle, scale, angle),
                "triangle": self.transform_points(PieceDrawer.triangle, scale, angle),
                "triangle2": self.transform_points(PieceDrawer.triangle2, scale, angle),
                "semicircle": self.transform_points(PieceDrawer.semicircle, scale, angle),
            }

    def transform_points(self, points, scale, angle):
        vectors = []

        for point in points:
            vector = Vector2(point)
            vector.scale_to_length(vector.magnitude() * scale)
            vector.rotate_ip(angle)
            vectors.append(vector)
        
        return vectors

    def deg_to_rad(self, degrees):
        return degrees * math.pi / 180

    def draw(self, edges):
        surface = Surface((self.render_size, self.render_size))
        surface.set_colorkey(WHITE)
        surface.fill(WHITE)

        drawer_x = self.start_offset
        drawer_y = self.start_offset
        angle = 0
        edge_end = Vector2(self.edge_length, 0)

        # Create polygon
        screen_points = []

        for edge in edges:
            if edge != None and edge.slot != "semicircle":
                shape = edge.slot
                
                self.add_points(screen_points, shape, edge.recessed, drawer_x, drawer_y, angle)

            # Finish edge
            drawer_x += edge_end.x
            drawer_y += edge_end.y

            screen_points.append(Vector2(drawer_x, drawer_y))

            angle += 90
            edge_end.rotate_ip(90)
            
        self.draw_poly(surface, screen_points, self.fill_color, self.border_color)

        # Draw semicircle edges
        drawer_x = self.start_offset
        drawer_y = self.start_offset
        angle = 0
        edge_end = Vector2(self.scale * PieceDrawer.BASE_LENGTH, 0)

        for edge in edges:
            if edge != None and edge.slot == "semicircle":
                self.draw_semicircle(surface, edge.recessed, drawer_x, drawer_y, angle, PieceDrawer.BASE_RADIUS)

            drawer_x += edge_end.x
            drawer_y += edge_end.y
            angle += 90
            edge_end.rotate_ip(90)
        
        return surface

    def add_points(self, point_list, shape, recessed, x1, y1, angle):
        points = self.shapes[angle][shape]
        invert_x = 1; invert_y = 1

        if not recessed:
            # top and bottom
            if angle == 0 or angle == 180:
                invert_y = -1
            # right and left
            elif angle == 90 or angle == 270:
                invert_x = -1
        
        for point in points:
            x = x1 + invert_x * point.x
            y = y1 + invert_y * point.y
            point_list.append(Vector2(x, y))

    def draw_poly(self, surface, points, fill_color, border_color):
        draw.polygon(surface, fill_color, points) # fill
        draw.lines(surface, border_color, True, points, PieceDrawer.BORDER_WIDTH) # border

    def draw_semicircle(self, surface, recessed, x1, y1, angle, radius):
        scaled_radius = radius * self.scale
        center = self.shapes[angle]["semicircle"][0]
        x = x1 + center.x
        y = y1 + center.y

        size = 2 * scaled_radius
        bounds = Rect(x - scaled_radius, y - scaled_radius, size, size)
        arc_start = self.deg_to_rad(angle if angle == 0 or angle == 180 else angle - 180)
        arc_end = self.deg_to_rad(angle + 180 if angle == 0 or angle == 180 else angle)
        
        if recessed:
            draw.circle(surface, WHITE, (x, y), scaled_radius) # fill

            arc_start += math.pi
            arc_end += math.pi
            
            draw.arc(surface, self.border_color, bounds, arc_start, arc_end, PieceDrawer.BORDER_WIDTH) # border
        else:
            draw.circle(surface, self.fill_color, (x, y), scaled_radius) # fill
            draw.arc(surface, self.border_color, bounds, arc_start, arc_end, PieceDrawer.BORDER_WIDTH) # border