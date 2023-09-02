import os
import sys

import pygame as pg


class GameManager:
    """Class that manages the game."""

    def __init__(self):
        """Initialize the game manager."""
        pg.init()
        flags = pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE | pg.SCALED | pg.SHOWN
        self.size = (800, 600)
        self.screen = pg.display.set_mode(self.size, flags=flags, vsync=1)
        pg.display.set_caption("Game")
        self.clock = pg.time.Clock()
        self.running = True

    def new_game(self):
        """Start a new game."""
        pass

    def update(self):
        """Update the game."""
        pg.display.flip()
        self.clock.tick(60)

    def draw(self):
        """Draw the game."""
        pass

    def check_events(self):
        """Check for events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()
            elif os.getenv('DEBUG').lower() == 'true' and (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.quit_game()

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
