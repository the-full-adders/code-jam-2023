from typing import TYPE_CHECKING

import pygame
import pygame_gui
from pygame_gui import UIManager as PygameUIManager

from .. import config as config
from .main_menu import MainMenu

if TYPE_CHECKING:
    from ..manager.game_manager import GameManager


class UIManager(PygameUIManager):
    """Class that manages the UI."""

    def __init__(self, gm: 'GameManager', *args, **kwargs):
        """Initialize the UI manager."""
        self.gm = gm
        super().__init__((gm.width, gm.height), str(config.PROJECT_DIR / "ui" / "theme.json"), *args, **kwargs)
        self.main_menu: MainMenu | None = None
        self.active_screen = "main_menu"
        self.ui_setup()

    def ui_setup(self):
        """Set up the UI manager."""
        self.setup_main_menu()

    def setup_main_menu(self):
        """Set up the main menu."""
        main_menu_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, self.gm.width*0.3, self.gm.height*0.6),
            manager=self,
            anchors={'center': 'center'},
            margins={'left': 0, 'right': 0, 'top': 10, 'bottom': 10},
            visible=True,
            object_id="main_menu_container"
        )
        main_menu_container.border_width = 0
        self.main_menu = MainMenu(main_menu_container, self)
        print("Main menu set up!")

    def process_button_pressed(self, event):
        """Process a button press."""
        if self.active_screen == "main_menu":
            match event.ui_object_id.split(".")[-1]:
                case "start_game_button":
                    print('Start Game button pressed')
                case "options_button":
                    print('Options button pressed')
                case "quit_button":
                    print('Quit button pressed')
                    self.gm.quit_game()