import requests

BASE = "https://environment.data.gov.uk/hydrology/id"
STATION_REF = "HIPPER_PARK ROAD BRIDGE_E_202312"
TARGETS = ["dissolved oxygen", "conductivity"]


def get_json(url, params=None):
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()["items"]


# --- find station from reference ---
stations = get_json(f"{BASE}/stations", {"search": STATION_REF})
station_id = stations[0]["notation"]

# --- get full station details ---
station = get_json(f"{BASE}/stations/{station_id}")[0]

print("Station:", station["label"])
print("River:", station.get("riverName"))

# --- filter required measures ---
measures = [
    m for m in station["measures"]
    if any(t in m["label"].lower() for t in TARGETS)
   ##  Add an exclusion condition to  removes the percent dissolved oxygen measure
   
   ## and "dissolved oxygen (%)" not in m["label"].lower()

]

# --- fetch latest readings ---
for m in measures:
    print("\nParameter:", m["label"])

    readings = get_json(f"{m['@id']}/readings", {"_sort": "-dateTime", "_limit": 10})

    for r in readings:
        print(r["dateTime"], "=", r["value"])