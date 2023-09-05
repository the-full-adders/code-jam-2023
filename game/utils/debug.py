from functools import lru_cache

import pygame


def draw_fps(font: pygame.font.Font, screen: pygame.Surface, clock: pygame.time.Clock):
    """Draw the FPS on the screen."""
    fps = font.render(f"FPS: {clock.get_fps():.2f}", True, [255, 255, 255], [0, 0, 0])
    screen.blit(fps, [0, 0])


def draw_text(text, font: pygame.font.Font, screen: pygame.Surface):
    """Draw text on the screen."""
    text = font.render(f"{text}", True, [255, 255, 255], [0, 0, 0])
    screen.blit(text, [0, 20])


@lru_cache(maxsize=1)
def print_on_change(value):
    """Print a value only when it changes."""
    print(value)
