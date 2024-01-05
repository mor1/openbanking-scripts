#!/usr/bin/env python3

# scrape endpoints from Confluence page now that participant_store.json
# is not maintained

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json
import datetime

URL = 'https://openbanking.atlassian.net/wiki/spaces/DZ/pages/1165263140/Open+Data+API+Dashboard/'
ID_RE = 'OpenDataAPIDashboard-ProductInformation.*'

if __name__ == '__main__':
    with requests.Session() as session:
        page = session.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        rows = soup.find('h2', {"id": re.compile(ID_RE)}).parent.select("table tr")
        for i, row in enumerate(rows):
            cols = row.select("td a")
            if len(cols) == 0: continue

            name = row.select("td")[0].text
            hrefs = list(map(lambda a: a['href'], cols))

            print(json.dumps({
                "name": name,
                "urls": hrefs,
                "mtime": datetime.datetime.now().isoformat(),
            }))
