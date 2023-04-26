from bs4 import BeautifulSoup
import pandas as pd
import requests
from typing import Dict, List

# url = "http://www.evergabe-online.de/search.html?3-1.0-searchPanel-searchForm-submitButton"
# https://www.evergabe-online.de/search.html?searchString=Ausbildung&publishDateRange=ALL
# r = requests.post(url, data=query_params)
# url = "http://www.evergabe-online.de/search.html?3-3.0-searchPanel-searchForm-submitButton"
# payload = {"searchLinkModal:input": "http://www.evergabe-online.de/search.html?searchString=Ausbildung&publishDateRange=ALL", "submitButton":1}
url = "http://www.evergabe-online.de/search.html"
headers = {"Content-Type": "application/json"}
query_params = {"searchString": "Ausbildung", "publishDateRange": "ALL"}
r = requests.get(url, headers=headers,  params=query_params)
print(r.text)
# results = data["results"]
# print(f"has more: {data['has_more']}")
# print(f"next cursor: {data['next_cursor']}")
parser = BeautifulSoup(r.text, "html.parser")

table = parser.find("table", class_="table-advanced table table-striped table-bordered")
footer = parser.find("tfoot")

column_names = ["topic", "contracting_authority", "place_of_delivery"]
df = pd.DataFrame(columns=column_names)


def extract_row(list_of_tds: List) -> Dict:
    topic = list_of_tds[0].text.strip()
    contracting_authority = list_of_tds[1].text.strip()
    place_of_delivery = list_of_tds[2].text.strip()

    return dict(zip(column_names, [topic, contracting_authority, place_of_delivery]))


for row in table.tbody.find_all("tr"):
    columns = row.find_all("td")

    if columns:
        row_as_dict = extract_row(columns)
        df = df.append(row_as_dict, ignore_index=True)

print(df.head())
print(df.shape)
