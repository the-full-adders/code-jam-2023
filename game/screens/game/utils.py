import math
from countries import Country
import pygame as pg

def pos2angle(A, B, aspectRatio):
    """Calculate the angle between two points."""
    x = B[0] - A[0]
    y = B[1] - A[1]
    angle = math.atan2(-y, x / aspectRatio)
    return angle


def draw_arcs(countries: tuple[Country, Country], curve_height: int, num_segments: int, color: tuple[int, int, int],
              screen: pg.Surface):

    countries_points: list[list[int, int], list[int, int]] = []
    for country in countries:
        countries_points.append(country.get_random_point())

    x1, y1 = countries_points[0]
    x2, y2 = countries_points[1]

    dx = (x2 - x1) / num_segments
    dy = (y2 - y1) / num_segments

    for i in range(num_segments + 1):
        t = i / num_segments
        x = x1 + dx * i
        y = y1 + dy * i - curve_height * math.sin(t * math.pi)

        pg.draw.circle(screen, color, (int(x), int(y)), 2)
