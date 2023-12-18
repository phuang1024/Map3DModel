"""
Use open-elevation to get elevation data.
"""

import time
import json

import requests
from tqdm import tqdm

LONG_MIN = -122.0658
LONG_MAX = -122.0456
LAT_MIN = 37.2780
LAT_MAX = 37.2873
RES = 5e-5

BATCH_SIZE = 38
DELAY = 1   # Don't overload the server


def generate_points():
    est_steps = int((LONG_MAX - LONG_MIN) / RES)
    pbar = tqdm(total=est_steps)

    long = LONG_MIN
    while long <= LONG_MAX:
        pbar.update(1)

        lat = LAT_MIN
        while lat <= LAT_MAX:
            yield (lat, long)
            lat += RES
        long += RES


def main():
    points = generate_points()

    while True:
        batch = []
        for _ in range(BATCH_SIZE):
            try:
                batch.append(next(points))
            except StopIteration:
                break

        if not batch:
            break

        url = "https://api.open-elevation.com/api/v1/lookup?locations="
        for lat, long in batch:
            url += f"{lat:.6f},{long:.6f}|"
        url = url[:-1]

        response = requests.get(url)
        data = response.json()

        # TODO save data.
        for result in data["results"]:
            print(result["elevation"])

        time.sleep(DELAY)
        break # TODO


if __name__ == "__main__":
    main()
