#one command execution
from api_client import get_station_data
from database import create_tables, insert_station, insert_measurements


def run_pipeline():

    print("Creating database...")
    create_tables()

    print("Extracting data from API...")
    station, measurements = get_station_data()

    print("Loading station...")
    insert_station(station)

    print("Loading measurements...")
    for m in measurements:
        insert_measurements(
            station["notation"],
            m["parameter"],
            m["unit"],
            m["readings"]
        )

    print("Pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()