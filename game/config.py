from pathlib import Path
from typing import List, TypedDict


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
}
