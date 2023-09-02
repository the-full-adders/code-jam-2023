import os
import sys

import pygame as pg
import pygame_gui as pgui

from .. import config as config
from ..ui.manager import UIManager


class GameManager:
    """Class that manages the game."""

    def __init__(self):
        """Initialize the game manager."""
        pg.init()
        flags = pg.SCALED | pg.SHOWN | pg.RESIZABLE
        self.width, self.height = 800, 600
        self.screen = pg.display.set_mode([self.width, self.height], flags=flags, vsync=1)
        self.font = pg.font.Font(
            str(config.PROJECT_DIR / 'assets' / 'fonts' / 'QuinqueFive.woff'),
            20
        )
        self.clock = pg.time.Clock()
        self.ui_manager: UIManager = None
        self.timedelta = 0
        pg.display.set_caption("cj-10-game")
        self.running = True

    def new_game(self):
        """Start a new game."""
        self.ui_manager = UIManager(self)

    def update(self):
        """Update the game."""
        pg.display.flip()
        self.timedelta = self.clock.tick(60) / 1000.0
        self.ui_manager.update(self.timedelta)

    def draw(self):
        """Draw the game."""
        self.screen.fill([0, 0, 0])
        self.ui_manager.draw_ui(self.screen)
        pg.display.update()

    def check_events(self):
        """Check for events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()
            elif os.getenv('DEBUG').lower() == 'true' and (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.quit_game()

            if event.type == pgui.UI_BUTTON_PRESSED:
                if self.ui_manager.active_screen == "main_menu":
                    if event.ui_element == self.ui_manager.main_menu.buttons['Start Game']:
                        print('Start Game button pressed')
                    elif event.ui_element == self.ui_manager.main_menu.buttons['Options']:
                        print('Options button pressed')
                    elif event.ui_element == self.ui_manager.main_menu.buttons['Quit']:
                        print('Quit button pressed')
                        self.quit_game()

            self.ui_manager.process_events(event)

    def run(self):
        """Run the game."""
        self.new_game()
        while self.running:
            self.check_events()
            self.update()
            self.draw()

    def quit_game(self):
        """Quits the game."""
        self.running = False
        pg.quit()
        sys.exit()
