from typing import Tuple

from pygame.color import Color


def hex2rgb(color_hex: str) -> Tuple[int, int, int]:
    """Converts a hex color to rgb."""
    c = Color(color_hex)
    return c.r, c.g, c.b
