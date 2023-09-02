from typing import TYPE_CHECKING

import pygame
import pygame_gui
from pygame_gui import UIManager as PygameUIManager

from .. import config as CONFIG
from .main_menu import MainMenu

if TYPE_CHECKING:
    from ..manager.game_manager import GameManager


class UIManager(PygameUIManager):
    """Class that manages the UI."""

    def __init__(self, gm: 'GameManager', *args, **kwargs):
        """Initialize the UI manager."""
        self.gm = gm
        super().__init__((gm.width, gm.height), str(CONFIG.PROJECT_DIR / "ui" / "theme.json"), *args, **kwargs)
        self.ui_setup()
        self.active_menu = None

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
            visible=True
        )
        main_menu_container.border_width = 0
        MainMenu(main_menu_container, self)
        self.active_menu = main_menu_container
