import os
import sys

import pygame as pg
import pygame_gui as pgui

from .. import config as config
from ..screens.game.world_map import Cursor, WorldMap
from ..ui.manager import UIManager
from ..utils.debug import draw_fps


class GameManager:
    """Class that manages the game."""

    def __init__(self):
        """Initialize the game manager."""
        pg.init()
        pg.mouse.set_visible(False)
        self.flags = pg.DOUBLEBUF | pg.SCALED | pg.SHOWN | pg.RESIZABLE
        self.width, self.height = config.ROOT_SVG['width'] + 10, config.ROOT_SVG['height'] + 10
        self.screen = pg.display.set_mode([self.width, self.height], flags=self.flags, vsync=1)
        self.font = pg.font.Font(
            str(config.PROJECT_DIR / 'assets' / 'fonts' / 'QuinqueFive.woff'),
            20
        )
        self.clock = pg.time.Clock()
        self.ui_manager: UIManager = UIManager(self)
        self.timedelta = 0
        pg.display.set_caption("cj-10-game")
        self.world_map: WorldMap = WorldMap(self, config.COLORS['bg'], visible=False, debug=False)
        self.running = True
        self.cursor = Cursor()

    def new_game(self):
        """Start a new game."""
        self.world_map.load_map()
        self.ui_manager.setup_game_screen()

    def check_events(self):
        """Check for events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()
            elif os.getenv('DEBUG').lower() == 'true' and (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.quit_game()

            if self.world_map.visible and event.type != pg.USEREVENT:
                self.world_map.process_events(event)
            # if event.type == pg.VIDEORESIZE:
            #     # There's some code to add back window content here.
            #     self.screen = pg.display.set_mode([event.w, event.h], self.flags)

            self.ui_manager.process_events(event)
            if event.type == pgui.UI_BUTTON_PRESSED:
                self.ui_manager.process_button_pressed(event)

    def update(self):
        """Update the game."""
        pg.display.flip()
        self.timedelta = self.clock.tick(60) / 1000.0
        self.cursor.update()
        self.ui_manager.update(self.timedelta)

    def draw(self):
        """Draw the game."""
        self.screen.fill(config.COLORS['bg'])
        self.ui_manager.draw_ui(self.screen)
        self.world_map.draw()

        if os.getenv('DEBUG').lower() == 'true':
            draw_fps(self.font, self.screen, self.clock)
        self.screen.blit(self.cursor.image, self.cursor.rect)
        pg.display.flip()

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
