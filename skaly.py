__title__ = "Skaly"
__version__ = "2.0"
__author__ = "Bartek Blachura"

"""
saves coordinates from topo.portalgorski.pl to kml file (divided into areas)
"""

from scraping import make_placemarks
from crawling import return_rocks
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from replace_non_ascii import removeAccents


def return_areas(url):
    user_agent = generate_user_agent(os=("mac", "linux", "win"))
    headers = {"user-agent": user_agent}

    areas_list = []

    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")

    for leafs in (soup.find_all("li", "leaf")):
        areas_list.append(url+(str(leafs).split("\"")[3]))

    return(areas_list)


def import_list(name):
    filepath = "{}.txt".format(name)
    imp_list = []

    with open(filepath, "r") as file:
        for line in file:
            imp_list.append(line[0:-1])
        return(imp_list)


def export_list(name, lines):
    filepath = "{}.txt".format(name)
    lines = [line + "\n" for line in lines]

    with open(filepath, "w") as file:
        file.writelines(lines)


def create_kml(name):
    filepath = "{}.kml".format(name)

    with open(filepath, "w") as kml:
        kml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        kml.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        kml.write('<Document>\n')
        kml.write('<name>{}</name>\n'.format(name))


def end_kml(name):
    filepath = "{}.kml".format(name)

    with open(filepath, "a") as kml:
        kml.write('</Document>\n')
        kml.write('</kml>')

    print()
    print("{} file has been successfully created!".format(filepath))


url = "http://www.topo.portalgorski.pl"

print("{} version {} by {} - saves rocks coordinates from topo.portalgorski.pl to .kml file.".format(__title__, __version__, __author__))

areas = return_areas(url)

for i in range(0, len(areas)):

    print()
    area_name = (removeAccents(areas[i].split("/")[3].split(",")[0]))
    print(area_name)

    rocks = return_rocks(url, areas[i])
    export_list(area_name, rocks)

    create_kml(area_name)

    for rock in rocks:
        make_placemarks(rock, area_name)

    end_kml(area_name)
