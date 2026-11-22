import requests
import time
import pandas as pd
# season, round, circuitId, driverId, constructorId, session, position, points, status
def page_to_rows(data, session):
    rows = []
    if session == "sprint":
        result_type = "SprintResults"
    elif session == "race":
        result_type = "Results"
    else:
        raise ValueError(f"Invalid session: '{session}'")
    for race in data["MRData"]["RaceTable"]["Races"]:
        for result in race[result_type]:
            row = {
                "season": int(race["season"]),
                "round": int(race["round"]),
                "circuitId": race["Circuit"]["circuitId"],
                "driverId": result["Driver"]["driverId"],
                "constructorId": result["Constructor"]["constructorId"],
                "session": "session",
                "position": int(result["position"]),
                "points": float(result["points"]),
                "status": result["status"]
            }
            rows.append(row)
    return rows
def get_json(url):
    time.sleep(1)
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code} and url {url}")
    return response.json()
def fetch_season(season, session):
    limit = 100
    offset = 0
    if session == "sprint":
        endpoint = "sprint"
    elif session == "race":
        endpoint = "results"
    else:
        raise ValueError(f"Invalid session: '{session}'")
    url = f"https://api.jolpi.ca/ergast/f1/{season}/{endpoint}.json?limit={limit}&offset={offset}"
    data = get_json(url)
    rows = page_to_rows(data, session)
    total = int(data["MRData"]["total"])
    for offset in range(limit, total, limit):
        url = f"https://api.jolpi.ca/ergast/f1/{season}/{endpoint}.json?limit={limit}&offset={offset}"
        data = get_json(url)
        page_rows = page_to_rows(data, session)
        rows.extend(page_rows)
    return rows
all_rows = []
for season in range(2014, 2026 + 1):
    for session in ["sprint", "race"]:
        print(f"Fetching season {season}/{session}")
        rows = fetch_season(season, session)
        all_rows.extend(rows)
df = pd.DataFrame(all_rows)
df.to_csv("data/results.csv", index=False)
