import requests

BASE = "https://environment.data.gov.uk/hydrology/id"
STATION_REF = "HIPPER_PARK ROAD BRIDGE_E_202312"
TARGETS = ["conductivity", "dissolved oxygen (mg/l)"]


def get_json(url, params=None):
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()["items"]


def get_station_data():

    stations = get_json(f"{BASE}/stations", {"search": STATION_REF})
    station_id = stations[0]["notation"]

    station = get_json(f"{BASE}/stations/{station_id}")[0]

    measures = [
        m for m in station["measures"]
        if any(t in m["label"].lower() for t in TARGETS)
    ]

    results = []

    for m in measures:
        readings = get_json(f"{m['@id']}/readings", {"_sort": "-dateTime", "_limit": 10})

        results.append({
            "parameter": m["label"],
            "unit": m["unitName"],
            "readings": readings
        })

    return station, results