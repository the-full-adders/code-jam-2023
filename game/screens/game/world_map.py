import json
from typing import TYPE_CHECKING, List

import pygame

from ... import config
from ...utils.debug import draw_text
from .countries import Country

if TYPE_CHECKING:
    from ...manager.game_manager import GameManager


class Cursor(pygame.sprite.Sprite):
    """Class that represents the cursor that is used in the game.

    # todo: Maybe this should be moved to the game manager class.
    """

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.rect = self.image.get_rect()
        self.color = [255, 0, 0]
        self.image.fill(self.color)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        """Update the position of the cursor."""
        self.rect.center = pygame.mouse.get_pos()
        self.image.fill(self.color)


class WorldMap:
    """Class that represents the world map."""

    def __init__(
            self,
            game_manager: 'GameManager',
            background_color: list,
            visible: bool = True,
            debug: bool = False
    ):
        if background_color is None:
            background_color = config.COLORS['bg']
        self._ASSETS_DIR = config.ASSETS_DIR / 'world_map'
        self.gm = game_manager

        self.world_surface = pygame.Surface([config.ROOT_SVG['width'], config.ROOT_SVG['height']])
        self.countries = pygame.sprite.Group()
        self.scale = 0.9
        self.background_color = background_color

        self._debug = debug
        self._map_drawn = False
        self.visible = visible

    @property
    def visible(self):
        """Get the visibility of the world map."""
        return self._visible

    @visible.setter
    def visible(self, value):
        """Set the visibility of the world map."""
        self._visible = value

    def load_map(self):
        """Load the world map.

        Ideally, this should be called only once.
        loads the svg file(s) and generates the countries sprites.
        """
        self.countries.add(*self._generate_countries_sprites())
        self.visible = True

    def _generate_countries_sprites(self) -> List[Country]:
        """Generate the countries sprites.

        Ideally, this should be called only once.
        """
        with open(self._ASSETS_DIR / 'country_coordinates.json', 'r') as f:
            country_coordinates = json.load(f)
        svgs = self._ASSETS_DIR.glob("countries_svgs/*.svg")
        countries = []
        for svg in svgs:
            cid = svg.stem
            country = Country(
                country_coordinates[cid]['x'],
                country_coordinates[cid]['y'],
                [
                    country_coordinates[cid]['width'],
                    country_coordinates[cid]['height']
                ],
                svg,
            )
            countries.append(country)
        return countries

    def blit_world_map(self):
        """Blit the world map on screen."""
        self.world_surface.fill(self.background_color)
        sprite: Country
        for sprite in self.countries:
            sprite.draw_country_border(self.world_surface)
        self.countries.draw(self.world_surface)  # todo: add a way to draw debug rects
        surface_draw_size = [
            dimension * self.scale
            for dimension in self.world_surface.get_size()
        ]
        pygame.transform.scale(
            self.world_surface,
            surface_draw_size,
        )
        self.gm.screen.blit(
            self.world_surface,
            self.world_surface.get_rect(
                center=self.gm.screen.get_rect().center
            )
        )
        self._map_drawn = True

    def draw(self):
        """Draws the world map."""
        if self.visible:
            # self.gm.screen.fill(self.background_color)
            self.blit_world_map()

    # def xy_collide_with_country(self, country_id: str, pos: List[int, int]) -> bool:
    #     """Check if the position collides with a country."""
    #     country_surface = self.countries_surfaces[country_id]

    def process_events(self, events):
        """Process events for the world map."""
        if pygame.sprite.spritecollideany(self.gm.cursor, self.countries,) and (
                country := pygame.sprite.spritecollideany(self.gm.cursor, self.countries, pygame.sprite.collide_mask)):
            # only do mask collision if rect collision is true
            draw_text(
                country.name, self.gm.font, self.gm.screen
            )
