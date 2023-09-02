import requests
from bs4 import BeautifulSoup

svgs_url = "https://malivinayak.github.io/world-map/"

r = requests.get(svgs_url)
soup = BeautifulSoup(r.content, "html.parser")

anchor_tags = soup.findAll("a")

for anchor in anchor_tags:
    paths = anchor.find_all("path")

    with open(f"assets/{anchor['xlink:title']}.svg", "w") as f:
        f.write("""<svg xmlns="http://www.w3.org/2000/svg">\n""")
        for path in paths:
            f.write(f"{path}\n")
        f.write("</svg>")
