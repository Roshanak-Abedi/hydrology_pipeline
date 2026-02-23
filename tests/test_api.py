import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import get_station_data


def test_get_station_data_returns_two_parameters_with_readings():
    station, measurements = get_station_data()

    assert station is not None
    assert "notation" in station
    assert "label" in station

    # Expect at least conductivity and dissolved oxygen (mg/L)
    assert len(measurements) >= 2

    for m in measurements:
        assert "parameter" in m
        assert "unit" in m
        assert "readings" in m
        assert len(m["readings"]) == 10

        for r in m["readings"]:
            assert "dateTime" in r
            assert "value" in r