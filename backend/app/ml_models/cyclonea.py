import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

years = range(2010, 2024)
cyclones = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0 Safari/537.36"
}

def clean_name(name: str) -> str:
    """
    Removes prefixes like 'Cyclone', 'Storm', 'Depression' etc.
    Returns only the short name (e.g., 'Biparjoy').
    """
    # Drop text inside brackets or footnotes
    name = re.sub(r"\[.*?\]", "", name)

    # Remove storm classifications
    for word in [
        "Cyclone", "Storm", "Typhoon", "Hurricane", "Depression",
        "Low", "Severe", "Extremely", "Very", "Super", "Tropical",
        "Deep", "Remnant"
    ]:
        name = name.replace(word, "")

    # Trim whitespace
    return name.strip()

for year in years:
    url = f"https://en.wikipedia.org/wiki/{year}_North_Indian_Ocean_cyclone_season"
    print(f"Fetching {url} ...")
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print(f"❌ Could not fetch {url}")
        continue

    soup = BeautifulSoup(res.text, "html.parser")
    tables = soup.find_all("table", {"class": "wikitable"})

    for table in tables:
        rows = table.find_all("tr")
        for row in rows[1:]:
            cols = [c.get_text(" ", strip=True) for c in row.find_all(["td", "th"])]

            if len(cols) < 2:
                continue

            name = clean_name(cols[0])
            if not name or len(name.split()) > 2:  # skip unnamed entries
                continue

            date_text = cols[1]
            match = re.findall(r"(\w+\s+\d{1,2})", date_text)

            if len(match) == 1:
                start_date = match[0] + f" {year}"
                end_date = match[0] + f" {year}"
            elif len(match) >= 2:
                start_date = match[0] + f" {year}"
                end_date = match[1] + f" {year}"
            else:
                continue

            start = pd.to_datetime(start_date, errors="coerce")
            end = pd.to_datetime(end_date, errors="coerce")

            if pd.isna(start) or pd.isna(end):
                continue

            cyclones.append([name, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")])

# Convert to DataFrame and drop duplicates
df = pd.DataFrame(cyclones, columns=["name", "start_date", "end_date"]).drop_duplicates()

df.to_csv("cyclones.csv", index=False)
print("✅ Saved cyclones.csv")
print(df.head(15))
