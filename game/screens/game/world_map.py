import json
from typing import TYPE_CHECKING

import pygame

from ... import config

if TYPE_CHECKING:
    from ...manager.game_manager import GameManager


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
            background_color = [127, 127, 127]
        self._ASSETS_DIR = config.ASSETS_DIR / 'world_map'
        self.gm = game_manager
        with open(self._ASSETS_DIR / 'country_coordinates.json', 'r') as f:
            self.country_coordinates = json.load(f)

        self.countries_surfaces = self._load_world_map()
        self.scale = 1
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

    def _load_world_map(self):
        svgs = self._ASSETS_DIR.glob("countries_svgs/*.svg")
        images = {}
        for svg in svgs:
            images[svg.stem.upper()] = pygame.image.load(str(svg)).convert_alpha()
        return images

    def blit_country(self, country: str, country_svg: pygame.Surface, scale: float = 1, debug: bool = False):
        """Blit country on screen,

        This seems to be a costly operation, hence use it only when needed
        more discussion about how to make this more efficient must be done
        """
        topleft = [self.country_coordinates[country]['x'], self.country_coordinates[country]['y']]
        size = [self.country_coordinates[country]['width'], self.country_coordinates[country]['height']]
        country_svg = pygame.transform.scale(country_svg, [size[0] * scale, size[1] * scale])
        country_svg.fill([0, 100, 200], special_flags=pygame.BLEND_MULT)
        self.gm.screen.blit(
            country_svg,
            country_svg.get_rect(
                topleft=topleft,
            )
        )
        if debug:
            pygame.draw.rect(self.gm.screen, [255, 0, 0], country_svg.get_rect(topleft=topleft), 1)

    def blit_world_map(self):
        """Blit the world map on screen."""
        for country, country_surface in self.countries_surfaces.items():
            self.blit_country(
                country=country,
                country_svg=country_surface,
                scale=self.scale,
                debug=self._debug
            )

    def process_events(self, events):
        """Process events for the world map."""
        pass

    def draw(self):
        """Draws the world map."""
        if self.visible:
            # self.gm.screen.fill(self.background_color)
            self.blit_world_map()

    def hide(self):
        """Hides the world map."""
        self.visible = False

    def show(self):
        """Shows the world map."""
        self.visible = True
