if True:
    import os
    os.environ['SDL_VIDEO_X11_WMCLASS'] = 'cj-10-game'
import json
from pathlib import Path
from typing import Dict

import pygame

try:
    import pycountry
    from lxml import etree
    from svgpathtools import svg2paths2, wsvg
except ImportError:
    print("Install deps in the 'extra' group to use this script")
    raise

assets_dir = Path(__file__).parent.parent / "assets" / "world_map"

with open(assets_dir / 'color_mapping.json') as f:
    color_mapping = json.load(f)

with open(assets_dir / 'country_coordinates.json') as f:
    country_coords = json.load(f)


def build_assets():
    """Split world map into countries"""
    # In this function we use svgpathtools to split the world map into countries
    # and save them as individual svg files. We then use clean_asset() to set
    # correct viewbox and size attributes for each country ( for reference see game/assets/country_coords.json ).
    # Further improvements could be made by using "bbox" function of path object to get the correct viewbox
    # hence removing the need for country_coords.json
    # todo: use svgpathtools bbox function of path object to get the correct viewbox
    paths, attributes, svg_attributes = svg2paths2("world_map.svg")
    for path, attribute in zip(paths, attributes):
        wsvg(path, attributes=[attribute], filename=f"assets/{attribute['id']}.svg")


def clean_asset():
    """Remove all non-essential characters from the asset name"""
    # In this function we use lxml to set correct viewbox and size attributes for each country
    # ( for reference see game/assets/country_coords.json ).
    svgs = assets_dir / "countries_svgs"
    svgs = svgs.glob("*.svg")
    for svg_file in svgs:
        country_id = svg_file.stem
        xml = etree.parse(svg_file)
        svg = xml.getroot()
        view_box = [
            country_coords[country_id]['x'],
            country_coords[country_id]['y'],
            country_coords[country_id]['width'],
            country_coords[country_id]['height'],
        ]
        svg.attrib['height'] = str(country_coords[country_id]['height'])
        svg.attrib['width'] = str(country_coords[country_id]['width'])
        svg.attrib['viewBox'] = " ".join([str(_) for _ in view_box])
        svg.attrib['fill'] = "#00394f"
        with open(svg_file, 'wb') as f:
            f.write(etree.tostring(xml, pretty_print=True))


def load_countries() -> Dict[str, pygame.Surface]:
    """Load all countries"""
    # go through all svg files in assets folder and load them as pygame surfaces
    # further discussion about how masks can be applied
    # to make an outline (ie: country borders) around image must be done.
    svgs = Path(__file__).parent.glob("assets/*.svg")
    images = {}
    for svg in svgs:
        images[svg.stem.upper()] = pygame.image.load(str(svg)).convert_alpha()
    return images


def fit_svg(filename: str):
    """Fit svg to window size"""
    # only to be used when a single image/svg is to be scaled down to fit the window
    svg_surface = pygame.image.load(filename).convert_alpha()
    size = svg_surface.get_size()
    scale = min(window.get_width() / size[0], window.get_width() / size[1]) * 0.9
    svg_surface = pygame.transform.scale(svg_surface, [size[0] * scale, size[1] * scale])
    return svg_surface, scale


def display_country_name(color):
    """Display country name on screen, 50px from bottom"""
    if color in color_mapping:
        country = pycountry.countries.get(alpha_2=color_mapping[color])
        if country:
            country = country.name
        else:
            country = color_mapping[color]
        text = font.render(country, True, green, blue)
        textRect = text.get_rect()
        textRect.center = (window.get_width() // 2, window.get_height() - 50)
        window.blit(text, textRect)


def blit_country(country: str, country_svg: pygame.Surface, scale: float = 1, debug: bool = False):
    """Blit country on screen,

    This seems to be a costly operation, hence use it only when needed
    more discussion about how to make this more efficient must be done
    """
    topleft = [country_coords[country]['x'], country_coords[country]['y']]
    size = [country_coords[country]['width'], country_coords[country]['height']]
    country_svg = pygame.transform.scale(country_svg, [size[0] * scale, size[1] * scale])
    country_svg.fill([0, 100, 200], special_flags=pygame.BLEND_MULT)
    window.blit(
        country_svg,
        country_svg.get_rect(
            topleft=topleft,
        )
    )
    if debug:
        pygame.draw.rect(window, [255, 0, 0], country_svg.get_rect(topleft=topleft), 1)


svg_size = country_coords['ROOT_SVG']
svg_size = [svg_size['width'], svg_size['height']]

pygame.init()
window = pygame.display.set_mode(svg_size)
clock = pygame.time.Clock()

locations = load_countries()
world_map_colored = fit_svg("world_color_mapped.svg")[0]
world_map = fit_svg("world_map.svg")[0]

run = True
font = pygame.font.Font('freesansbold.ttf', 32)
white = [255, 255, 255]
green = [0, 255, 0]
blue = [0, 0, 128]

# todo: find how to scale so that countries are always in order
scale = 1
window.fill([127, 127, 127])
for country, svg in locations.items():
    blit_country(country, svg, scale, debug=False)


while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # color = "#{:02X}{:02X}{:02X}".format(*world_map_colored.get_at([x,y])[:3]).lower()
    # display_country(last_color)

    pygame.display.flip()

pygame.quit()
exit()
