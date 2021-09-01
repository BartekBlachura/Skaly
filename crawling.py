import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent


def return_rocks(main_url, url):

    user_agent = generate_user_agent(os=("mac", "linux", "win"))
    headers = {"user-agent": user_agent}

    new_url_list = [url]
    rocks_url = []

    print("crawling...")

    for new_url in new_url_list:
        result = requests.get(new_url, headers=headers)
        soup = BeautifulSoup(result.text, "html.parser")

        print(new_url)

        for leafs in (soup.find_all("li", "leaf")):
            new_url_list.append(main_url+(str(leafs).split("\"")[3]))

        for coordinates in (soup.find_all("span", "dataSm")):
            i =+ 1
            if i != 0:
                rocks_url.append(new_url)
                print("Rock!")

    return(rocks_url)
