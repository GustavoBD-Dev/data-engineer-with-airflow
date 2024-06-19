import psycopg2
import requests
from bs4 import BeautifulSoup
import json


def scrape_tools():
    website = "https://www.moderndatastack.xyz/stacks"
    page = requests.get(website)
    soup = BeautifulSoup(page.page_source, 'html.parser')
    
    data_scrap = []

    for link in soup.find_all('h4'):

        link_text = str(link.text)

        if link_text.endswith(" "):
            link_text = str(link.text)[:-1]

        if link_text.lower() == 'angellist talent':
            link_text = 'angellist'
        elif link_text.lower() == "feeld":
            link_text = "fantastics"
        elif link_text.lower() == "hashboard":
            link_text = "glean"
        elif link_text.lower() == "l'oréal":
            link_text = "loreal"
        elif link_text.lower() == "circleup":
            link_text = "circleup-inc"

        print(link.text +':  ' +link_text.lower())
        url_get = f"https://www.moderndatastack.xyz/stacks/{str(link_text).lower().replace(' ','-').replace('&', '').replace('.','').replace(',','').replace('--','-').replace('(','').replace(')','')}"
        print(">>>" + url_get)
        page_2 = requests.get(url_get)
        page_2.get(url_get)
        soup_2 = BeautifulSoup(page_2.page_source, 'html.parser')
        st_dict = {}

        for tools in soup_2.find_all('div', 'p-3 row'):
            for vendors in tools.find_all('h4'):
                x = vendors.text #[x for x in vendors.contents]
                y = [x.text for x in tools.find_all('p')]
                st_dict[x] = y
                print(x)
                print(y)

        enterprise = str(link_text).lower().replace(' ','-').replace('&', '').replace('.','').replace(',','').replace('--','-').replace('(','').replace(')','').capitalize()
        data = {}
        data = {'name': enterprise, 'tools': st_dict}
        print(data)
        data_scrap.append(data)

        # Convert the dictionary to a JSON string
        json_string = json.dumps(data_scrap)


        # create table

        # populate table