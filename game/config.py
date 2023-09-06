from pathlib import Path
from typing import List, TypedDict

from .utils import helpers


class RootSVG(TypedDict):
    """Type definition for the root svg"""

    x: float
    y: int
    width: float
    height: float
    center: List[float]


PROJECT_DIR = Path(__file__).parent
ASSETS_DIR = PROJECT_DIR / "assets"

# from game/assets/country_coords.json
# used to set initial size of pygame window

ROOT_SVG: RootSVG = {
    'x': 1.1540000438690186,
    'y': 0,
    'width': 1009.114990234375,
    'height': 665.2420043945312,
    'center': [
        505.154000043869,
        332.0
    ]
}

COLORS = {
    'bg': [1, 23, 27],
    'fg': list(helpers.hex2rgb("#00394f")),
    
}

# Color Palette for future reference
# colors = [
#     ("Midnight Blue", [0, 57, 79]),
#     ("Deep Sea Blue", [0, 122, 150]),
#     ("Turquoise Blue", [54, 153, 173]),
#     ("Aquamarine", [124, 203, 214]),
#     ("Pale Green", [242, 255, 230]),
#     ("Light Yellow", [245, 233, 174]),
#     ("Olive Green", [207, 209, 121]),
#     ("Lime Green", [158, 186, 89]),
#     ("Forest Green", [102, 150, 63]),
#     ("Moss Green", [71, 102, 61])
# ]
# You can add more colors as needed
