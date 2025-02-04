import datetime
import json
from urllib.parse import quote

import requests

from ..helpers import CollectionAppointment

DESCRIPTION = "Source for PGH.ST services for the city of Pittsburgh, PA, USA."
URL = "http://www.pgh.st"
TEST_CASES = {}
TEST_CASES = {
    "Pittsburgh, Negley": {
        "house_number": 800,
        "street_name": "Negley",
        "zipcode": 15232,
    }
}


class Source:
    def __init__(self, house_number, street_name, zipcode):
        self._house_number = house_number
        self._street_name = street_name.replace(".", "").strip()
        self._zipcode = zipcode

    def fetch(self):
        # get json file
        r = requests.get(
            f"http://pgh.st/locate/{self._house_number}/{quote(self._street_name)}/{self._zipcode}"
        )

        # extract data from json
        data = json.loads(r.text)

        # create entries for trash, recycling, and yard waste
        entries = [
            CollectionAppointment(
                date=datetime.datetime.strptime(
                    data[0]["next_pickup_date"], "%m-%d-%Y"
                ).date(),
                t="Trash",
                icon="mdi:trash-can",
            ),
            CollectionAppointment(
                date=datetime.datetime.strptime(
                    data[0]["next_recycling_date"], "%m-%d-%Y"
                ).date(),
                t="Recycling",
                icon="mdi:recycle",
            ),
            CollectionAppointment(
                date=datetime.datetime.strptime(
                    data[0]["next_yard_date"], "%m-%d-%Y"
                ).date(),
                t="Yard Waste",
                icon="mdi:leaf",
            ),
        ]

        return entries
