import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from typing import Optional


def get_ci_for_interval(start_time, delta, postcode) -> tuple[str, Optional[float]]:
    """
    Retrieves carbon intensity forecast data for a specified time interval and postcode.

    Args:
        start_time (datetime): The start time of the interval (UTC).
        delta (timedelta): The duration of the interval.
        postcode (str): The UK postcode to query carbon intensity for, e.g. EC1A. This must be only the outward postcode (the first half of the full postcode).

    Returns:
        tuple[str, float]: A tuple containing the formatted start time (as a string) and the carbon intensity forecast (in gCO2/kWh).

    Raises:
        SystemExit: If the HTTP request to the API fails.
    """
    dateformat = "%Y-%m-%dT%H:%MZ"
    end_time = start_time + delta
    start_time_url = start_time.strftime(dateformat)
    end_time_url = end_time.strftime(dateformat)

    # Query carbonintensity to get the JSON information
    ci_url: str = f"https://api.carbonintensity.org.uk/regional/intensity/{start_time_url}/{end_time_url}/postcode/{postcode}"
    ci_response = None
    try:
        ci_response = urllib.request.urlopen(ci_url)
    except urllib.error.HTTPError as e:
        print(e)
        sys.exit(1)

    # Parse the JSON retrieved from the website
    ci_json = ci_response.read()
    ci_d = json.loads(ci_json)
    try:
        ci_value = ci_d["data"]["data"][0]["intensity"]["forecast"]
    except IndexError:
        print(f"No data available for {start_time}!")
        ci_value = None

    return start_time_url, ci_value


# Definitions for querying web API
LOCATION = "EC1A" # representing 'London' region
TIME_DELTA = timedelta(minutes=30)

parser = argparse.ArgumentParser(
    description="Retrieve carbon intensity values (gCO2/kWh), over half-hour intervals, for the location of CREATE HPC on a given day.",
    epilog="Carbon intensity data is retrieved from carbonintensity.org.uk.\n",
)
parser.add_argument(
    "date", type=str, help="Date to retrieve data for, in YYYY-MM-DD format."
)
parser.add_argument(
    "--dir",
    type=str,
    help="Path to output directory. Output .csv files will be created in subfolders in this directory, in the format `YYYY/MM/YYYYMMDD_ci.csv`",
)

args = parser.parse_args()
date_start = datetime.strptime(args.date, "%Y-%m-%d")
ci_data_dir = args.dir

interval_starts = [
    date_start + n * TIME_DELTA for n in range(0, 48)
]  # number of 30 min intervals in a day
interval_ci = [
    get_ci_for_interval(start_time, TIME_DELTA, LOCATION)
    for start_time in interval_starts
]

s_year = date_start.year
s_month = date_start.month
s_day = date_start.day

ci_dir = f"{ci_data_dir}/{s_year}/{s_month:02d}/"
ci_csv = os.path.join(ci_dir, f"{s_year}{s_month:02d}{s_day:02d}_ci.csv")
os.makedirs(ci_dir, exist_ok=True)

with open(ci_csv, "w") as csv_file:
    writer = csv.writer(csv_file)
    for row in interval_ci:
        writer.writerow(row)
