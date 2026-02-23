# Hydrology Data Pipeline

This project implements a simple data engineering pipeline (ETL-style) using the UK Hydrological Data Explorer API.

The pipeline:
- Connects to the Hydrological Data Explorer API
- Downloads the 10 most recent measurements for two parameters from station:
 `HIPPER_PARK ROAD BRIDGE_E_202312`
- Stores the data in a file-based SQLite database
- Uses a simplified star-schema style design 
- Runs from a single command after setup (`python main.py`)

Selected parameters:
- Conductivity
- Dissolved Oxygen (mg/L)

## Station

- Station reference: `HIPPER_PARK ROAD BRIDGE_E_202312`

## Project Structure

```text
hydrology_pipeline/
|-- api_client.py          # Extracts data from Hydrology API
|-- database.py            # SQLite schema creation and inserts
|-- main.py                # Pipeline entry point (single-command run)
|-- requirements.txt       # Project dependencies
|-- README.md              # Project documentation
|-- .gitignore             # Ignored files
|-- data/
|   |-- .gitkeep           # Placeholder to keep folder in Git
|   |-- hydrology.db       # SQLite database file (created after pipeline run, ignored)
|-- dev/                   # Exploratory scripts (not part of pipeline)
|   |-- api_exploration.py # Exploratory API script
|   |-- check_db.py        # Quick database inspection script
|   |-- check_api_connection.py
|-- tests/
|   |-- test_api.py
|   |-- test_database.py
```

Note:
- Local environment folders/files such as `venv/`, `__pycache__/`, `.pytest_cache/`, and `*.db` are ignored by `.gitignore`.
- The `data/` folder is kept in the repository using `data/.gitkeep`; `data/hydrology.db` is created at runtime.

## Installation (Windows / PowerShell)

1. Create a virtual environment:
```powershell
python -m venv venv
```

2. Activate the virtual environment

PowerShell (standard):
```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution (`not digitally signed`), use this temporary workaround (current terminal only):
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Alternative (no PowerShell execution policy change):
```powershell
.\venv\Scripts\activate.bat
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

## Run The Pipeline

Run with a single command:
```powershell
python main.py
```

What it does:
- Creates the SQLite database and tables
- Retrieves station metadata
- Retrieves the latest 10 readings for each selected parameter
- Prevents duplicate measurement rows on repeated runs (for the same reading timestamp and parameter)
- Loads station and measurement data into the database

Database output file:
- `data/hydrology.db`

## How "Latest 10" Is Retrieved

For each selected measure, the pipeline requests readings sorted by `dateTime` in descending order, then limits the result to 10 rows.

This ensures the returned rows are the most recent readings (newest first).

## Database Schema (Simplified Star-Schema Style)

This project follows the assignment's simplified schema approach using two tables.

### `stations` (task-oriented central/fact-like table)
Stores station metadata.

Columns:
- `station_id` (PRIMARY KEY)
- `name`
- `river`
- `latitude`
- `longitude`

### `measurements` (related measurement table)
Stores time-series readings linked to a station.

Columns:
- `id` (PRIMARY KEY)
- `station_id` (FOREIGN KEY -> `stations.station_id`)
- `parameter`
- `datetime`
- `value`
- `unit`
- Unique constraint: (`station_id`, `parameter`, `datetime`)
  to prevent duplicate readings on reruns

## Query The Database (Python)

Quick check using the included script:
```powershell
python dev/check_db.py
```

Example: show stored parameters and row counts
```powershell
python -c 'import sqlite3; conn=sqlite3.connect("data/hydrology.db"); cur=conn.cursor(); [print(row) for row in cur.execute("SELECT parameter, COUNT(*) FROM measurements GROUP BY parameter")]; conn.close()'
```

## Running Tests

Run tests with:
```powershell
pytest
```

Notes:
- `tests/test_database.py` checks database table creation
- `tests/test_api.py` calls the live API (network connection required)

## Notes / Assumptions

- The project is designed to be interview-task focused.
- The schema naming follows the task's simplified wording (station as the central table).
- Deduplication is handled at the SQLite layer using a composite unique constraint and `INSERT OR IGNORE`, which is more reliable than Python-only deduplication.
- The repository includes `data/.gitkeep` so the `data/` folder exists on clone and SQLite can create `data/hydrology.db` on first run.

## API Reference

Hydrological Data Explorer API documentation:
- https://environment.data.gov.uk/hydrology/doc/reference
