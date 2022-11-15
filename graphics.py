import math
import pygame
from pygame import rect, Vector2

class PieceSurface:
    BASE_LENGTH = 10
    BASE_RADIUS = 2
    SCALE = 6
    BORDER_WIDTH = 2

    square = [(4, 0), (4, 2), (6, 2), (6, 0)]
    rectangle = [(3, 0), (3, 2), (7, 2), (7, 0)]
    triangle = [(4, 0), (5, 2), (6, 0)]
    triangle2 = [(4, 0), (4, 2), (5, 0), (6, 2), (6, 0)]
    semicircle = [(5, 0)]

    def __init__(self, parent_surface, edges):
        self.parent_surface = parent_surface
        self.edges = edges

        self.shapes = {}

        self.fill_color = (255, 0, 0, 255)
        self.border_color = (0, 0, 0, 255)
        self.set_scale(PieceSurface.SCALE)

    def set_fill_color(self, color):
        self.fill_color = color

    def set_border_color(self, color):
        self.border_color = color

    def set_scale(self, scale):
        self.scale = scale

        for angle in [0, 90, 180, 270]:
            self.shapes[angle] = {
                "square": self.transform_point(PieceSurface.square, scale, angle),
                "rectangle": self.transform_point(PieceSurface.rectangle, scale, angle),
                "triangle": self.transform_point(PieceSurface.triangle, scale, angle),
                "triangle2": self.transform_point(PieceSurface.triangle2, scale, angle),
                "semicircle": self.transform_point(PieceSurface.semicircle, scale, angle),
            }

    def transform_point(self, points, scale, angle):
        vectors = []

        for point in points:
            vector = Vector2(point)
            vector.scale_to_length(vector.magnitude() * scale)
            vector.rotate_ip(angle)
            vectors.append(vector)
        
        return vectors

    def deg_to_rad(self, degrees):
        return degrees * math.pi / 180

    def render(self, position):
        x = position[0]
        y = position[1]
        angle = 0
        edge_end = Vector2(self.scale * PieceSurface.BASE_LENGTH, 0)

        # Create polygon
        screen_points = []

        for edge in self.edges:
            if edge != None and edge.slot != "semicircle":
                shape = edge.slot
                
                self.add_points(screen_points, shape, edge.recessed, x, y, angle)

            # Finish edge
            x += edge_end.x
            y += edge_end.y

            screen_points.append(Vector2(x, y))

            angle += 90
            edge_end.rotate_ip(90)
            
        self.draw_poly(screen_points)

        # Draw semicircle edges
        x = position[0]
        y = position[1]
        angle = 0
        edge_end = Vector2(self.scale * PieceSurface.BASE_LENGTH, 0)

        for edge in self.edges:
            if edge != None and edge.slot == "semicircle":
                self.draw_semicircle(edge.recessed, x, y, angle, PieceSurface.BASE_RADIUS)

            x += edge_end.x
            y += edge_end.y
            angle += 90
            edge_end.rotate_ip(90)

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
    
    def draw_poly(self, points):
        pygame.draw.polygon(self.parent_surface, self.fill_color, points) # fill
        pygame.draw.lines(self.parent_surface, self.border_color, True, points, PieceSurface.BORDER_WIDTH) # border

    def draw_semicircle(self, recessed, x1, y1, angle, radius):
        scaled_radius = radius * self.scale
        center = self.shapes[angle]["semicircle"][0]
        x = x1 + center.x
        y = y1 + center.y

        # border
        bounds = rect.Rect(x - scaled_radius, y - scaled_radius, 2 * scaled_radius, 2 * scaled_radius)
        arc_start = self.deg_to_rad(angle if angle == 0 or angle == 180 else angle - 180)
        arc_end = self.deg_to_rad(angle + 180 if angle == 0 or angle == 180 else angle)
        
        if recessed:
            # negative = pygame.surface.Surface((2 * scaled_radius, 2 * scaled_radius))
            # pygame.draw.circle(negative, self.fill_color, (scaled_radius, scaled_radius), scaled_radius) # negative fill
            # self.parent_surface.blit(negative, (x - scaled_radius, y - scaled_radius), self.parent_surface.get_rect(), special_flags=pygame.BLEND_SUB)
            pygame.draw.circle(self.parent_surface, (255, 255, 255), (x, y), scaled_radius) # fill

            arc_start += math.pi
            arc_end += math.pi
            
            pygame.draw.arc(self.parent_surface, self.border_color, bounds, arc_start, arc_end, PieceSurface.BORDER_WIDTH) # border
        else:
            pygame.draw.circle(self.parent_surface, self.fill_color, (x, y), scaled_radius) # fill
            pygame.draw.arc(self.parent_surface, self.border_color, bounds, arc_start, arc_end, PieceSurface.BORDER_WIDTH) # border