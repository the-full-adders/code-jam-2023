import random
from pathlib import Path

import pycountry
import pygame
from pygame.sprite import Sprite

from ...config import COLORS


class Country(Sprite):
    """Class that represents a country on the world map."""

    def __init__(self, x, y, size, country_svg: Path):
        super().__init__()
        self.fg_color = COLORS['fg']

        self.cid = country_svg.stem.upper()
        try:
            self.name = pycountry.countries.get(alpha_2=self.cid).name
        except AttributeError:
            self.name = self.cid
        self.image = pygame.image.load(str(country_svg)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [x-2, y+2]  # compensate for the border

        self.fitting_scale = 0.98
        self.image = pygame.transform.scale(self.image, [dimension * self.fitting_scale for dimension in size])

        self.mask = pygame.mask.from_surface(self.image)
        self.mask_surface: pygame.Surface | None = None
        self.connections = []

        self.border_color = [0, 0, 0]

    def draw_country_border(
            self,
            surface: pygame.Surface,
            border_color: list[int, int, int] = None,
            border_width: int = 1
    ):
        """Draw the border of the country."""
        if border_color:
            self.border_color = border_color

        self.mask_surface = self.mask.to_surface()
        self.mask_surface.set_colorkey([0, 0, 0])
        dx, dy = [1, -1, 0, 0], [0, 0, 1, -1]
        for x, y in zip(dx, dy):
            pos = [
                self.rect.x + x * border_width,
                self.rect.y + y * border_width
            ]
            surface.blit(self.mask_surface, pos)

    def process_events(self, events):
        """Process events sent by pygame for the country."""
        pass

    def get_random_point(self) -> list[int, int]:
        """Get a random position inside the country."""
        if not self.connections:
            x, y = (random.randint(0, self.mask_surface.get_rect().width),
                    random.randint(0, self.mask_surface.get_rect().height))
            while not self.mask_surface.get_at([x, y]):
                x, y = (random.randint(0, self.rect.width), random.randint(0, self.rect.height))
            self.connections.append([self.rect.x + x, self.rect.y + y])
        return self.connections[0]
