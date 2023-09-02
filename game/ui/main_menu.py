from typing import TYPE_CHECKING

import pygame
import pygame_gui

if TYPE_CHECKING:
    from .manager import UIManager


class MainMenu:
    """Class that represents the main menu."""

    def __init__(self, container: 'pygame_gui.elements.UIPanel', manager: 'UIManager'):
        self.manager = manager
        self.container = container
        self.buttons = []

        button_texts = [
            "Start Game",
            "Options",
            "Quit"
        ]
        spacing = 10
        container_rect = container.get_container()
        button_width = container_rect.get_size()[0] * 0.8
        y_margin = container.container_margins['top'] + container.container_margins['bottom']
        button_height = (container_rect.get_size()[1] - y_margin - 2*spacing) / len(button_texts)

        for index, button_text in enumerate(button_texts):
            button_options = {
                'relative_rect': pygame.Rect([0, (button_height+spacing)*index], [button_width, button_height]),
                'text': button_text,
                'manager': manager,
                'container': container,
                'anchors': {'centerx': 'centerx'},
            }
            self.buttons.append(pygame_gui.elements.UIButton(**button_options))
