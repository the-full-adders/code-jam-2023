from typing import TYPE_CHECKING, Literal, TypedDict, Union

import pygame
import pygame_gui
from pygame_gui import UIManager as PygameUIManager

from .. import config as config
from ..screens.game.world_map import WorldMap
from ..screens.main_menu import MainMenu
from ..screens.options_menu import OptionsMenu

if TYPE_CHECKING:
    from ..manager.game_manager import GameManager


class ScreensType(TypedDict):
    """Type that represents the screens."""

    main_menu: Union[MainMenu, None]
    options_menu: Union[OptionsMenu, None]
    game: Union[WorldMap, None]


class UIManager(PygameUIManager):
    """Class that manages the UI."""

    def __init__(self, gm: 'GameManager', *args, **kwargs):
        """Initialize the UI manager."""
        self.gm = gm
        super().__init__((gm.width, gm.height), str(config.PROJECT_DIR / "ui" / "theme.json"), *args, **kwargs)
        self.screens: ScreensType = {
            "main_menu": None,
            "options_menu": None,
            "game": None,
        }
        self.active_screen = "main_menu"
        self.ui_setup()

    @property
    def active_screen(self):
        """Get the active screen."""
        return self._active_screen

    @active_screen.setter
    def active_screen(self, value: Literal["main_menu", "options_menu", "game"]):
        # find a way to make Literal dynamic
        if value not in self.screens:
            raise ValueError(f"Screen {value} does not exist!")
        self._active_screen = value

    def ui_setup(self):
        """Set up the UI manager."""
        self.setup_main_menu()
        self.setup_options_menu()

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
        self.screens['main_menu'] = MainMenu(main_menu_container, self)
        print("Main menu set up!")

    def setup_options_menu(self):
        """Set up the options' menu."""
        container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, self.gm.width*0.3, self.gm.height*0.6),
            manager=self,
            anchors={'center': 'center'},
            margins={'left': 0, 'right': 0, 'top': 10, 'bottom': 10},
            visible=False,
            object_id="options_menu_container"
        )
        container.border_width = 0
        self.screens['options_menu'] = OptionsMenu(container, self)
        print("Options menu set up!")

    def setup_game_screen(self):
        """Set up the UI on game screen NOT THE GAME SCREEN ITSELF."""
        pass

    def process_button_pressed(self, event):
        """Process a button press."""
        # match the first part of the object id, which is the container
        match event.ui_object_id.split(".")[0]:
            case "main_menu_container":
                self.screens['main_menu'].process_button_pressed(event)
            case "options_menu_container":
                self.screens['options_menu'].process_button_pressed(event)
