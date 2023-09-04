import os
import sys

import pygame as pg
import pygame_gui as pgui

from .. import config as config
from ..screens.game.world_map import WorldMap
from ..ui.manager import UIManager


class GameManager:
    """Class that manages the game."""

    def __init__(self):
        """Initialize the game manager."""
        pg.init()
        flags = pg.SCALED | pg.SHOWN | pg.RESIZABLE
        self.width, self.height = config.ROOT_SVG['width'], config.ROOT_SVG['height']
        self.screen = pg.display.set_mode([self.width, self.height], flags=flags, vsync=1)
        self.font = pg.font.Font(
            str(config.PROJECT_DIR / 'assets' / 'fonts' / 'QuinqueFive.woff'),
            20
        )
        self.clock = pg.time.Clock()
        self.ui_manager: UIManager = UIManager(self)
        self.timedelta = 0
        pg.display.set_caption("cj-10-game")
        self.world_map: WorldMap | None = None
        self.running = True

    def new_game(self):
        """Start a new game."""
        self.world_map = WorldMap(self, config.COLORS['bg'], visible=True, debug=False)
        self.ui_manager.setup_game_screen()

    def update(self):
        """Update the game."""
        pg.display.flip()
        self.timedelta = self.clock.tick(60) / 1000.0
        self.ui_manager.update(self.timedelta)

    def draw(self):
        """Draw the game."""
        self.screen.fill(config.COLORS['bg'])
        self.ui_manager.draw_ui(self.screen)
        if self.ui_manager.active_screen == 'game':
            self.world_map.draw()
        pg.display.update()

    def check_events(self):
        """Check for events."""
        for event in pg.event.get():
            self.ui_manager.process_events(event)

            if event.type == pg.QUIT:
                self.quit_game()
            elif os.getenv('DEBUG').lower() == 'true' and (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.quit_game()

            if event.type == pgui.UI_BUTTON_PRESSED:
                self.ui_manager.process_button_pressed(event)

    def run(self):
        """Run the game."""
        while self.running:
            self.check_events()
            self.update()
            self.draw()

    def quit_game(self):
        """Quits the game."""
        self.running = False
        pg.quit()
        sys.exit()
