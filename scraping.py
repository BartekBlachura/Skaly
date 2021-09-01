import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from replace_non_ascii import removeAccents


def export_placemarks(lines, file_name):
    filepath = "{}.kml".format(file_name)

    lines = [removeAccents(line) + "\n" for line in lines]

    with open(filepath, "a") as temp:
        temp.writelines(lines)


def make_placemarks(url, file_name):

    user_agent = generate_user_agent(os=("mac", "linux", "win"))
    headers = {"user-agent": user_agent}
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")

    placemarks = ["<Placemark>"]

    print("scraping...")

    for name in (soup.find_all("h1")):
        name = ((str(name).split(">")[1]).split("<")[0])
        placemarks.append("<name>" + name + "</name>")

        print(name)

    description_url = ("<a href='{}'>{}</a>".format(url, url))
    placemarks.append("<description>" + description_url + "</description>")

    placemarks.append("<Point>")

    for coordinates in (soup.find_all("span", "dataSm")):
        latitude = ((str(coordinates).split(">")[1]).split("<")[0].split(" ")[0])
        longitude = ((str(coordinates).split(">")[1]).split("<")[0].split(" ")[2])
        coordinates = (longitude+","+latitude)
        placemarks.append("<coordinates>" + coordinates + "</coordinates>")

    placemarks.append("</Point>")
    placemarks.append("</Placemark>")

    export_placemarks(placemarks, file_name)
