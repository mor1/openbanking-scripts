#!/usr/bin/env python3

# scrape endpoints from Confluence page now that participant_store.json
# is not maintained

import datetime
import json
import logging

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.logging import RichHandler

errcon = Console(stderr=True)
logging.basicConfig(
    level="INFO",
    format="%(funcName)s:%(lineno)d %(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=errcon, rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

URL = "https://openbanking.atlassian.net/wiki/spaces/DZ/pages/1165263140/Open+Data+API+Dashboard/"
H2ID = r"Product Information & FCA Metrics"

if __name__ == "__main__":
    # log.setLevel(logging.DEBUG)

    with requests.Session() as session:
        page = session.get(URL)
        log.debug(f"{page=}")

        soup = BeautifulSoup(page.content, "html.parser")
        rows = soup.find("h2", string=H2ID)
        if not rows:
            log.fatal(f"couldn't find {H2ID}; {soup.find('h2').text=}")
        rows = rows.parent.parent.parent.parent.select("table tr")
        log.debug(f"{rows=}")

        for i, row in enumerate(rows):
            log.debug(f"{i=} {row=}")
            cols = row.select("td a")
            if len(cols) == 0:
                continue

            name = row.select("td")[0].text
            hrefs = list(map(lambda a: a["href"], cols))

            print(
                json.dumps(
                    {
                        "name": name,
                        "urls": hrefs,
                        "mtime": datetime.datetime.now().isoformat(),
                    }
                )
            )
