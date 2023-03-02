"""
Script to fetch event data from Uniswap V2 and V3.
"""

import os
import time
from config import constants
import environ.fetch.fetch_utils as utils
from environ.fetch.fetch_mints_v2 import fetch_mints_v2
from environ.fetch.fetch_mints_v3 import fetch_mints_v3


def fetch_main() -> None:
    """
    Aggregate all the fetch functions.
    """

    for event_info in [
        constants.EVENT_ONE,
        constants.EVENT_TWO,
        constants.EVENT_THREE,
        constants.EVENT_FOUR,
    ]:
        # convert the timestring to timestamp
        event_start_timestamp = utils.timestamp_converter(event_info[1])[
            "start_timestamp"
        ]
        event_end_timestamp = utils.timestamp_converter(event_info[1])["end_timestamp"]

        time.sleep(5)

        # info message
        print(
            f"Fetching v2 mint data for {event_info[0]} from {event_info[1]} "
            f"with timestamp {event_start_timestamp} to {event_end_timestamp}"
        )

        # fetch mints of Uniswap V2
        df_mints = fetch_mints_v2(event_start_timestamp, event_end_timestamp)

        # check if there is the path
        if not os.path.exists(constants.DATA_V2_PATH):
            os.makedirs(constants.DATA_V2_PATH)

        # save the data to Uniswap V2 directory
        df_mints.to_csv(
            f"{constants.DATA_V2_PATH}/{event_info[0]}_mints.csv", index=False
        )

        time.sleep(5)

        # info message
        print(
            f"Fetching v3 mints data for {event_info[0]} from {event_info[1]} "
            f"with timestamp {event_start_timestamp} to {event_end_timestamp}"
        )

        # fetch mints of Uniswap V3
        df_mints = fetch_mints_v3(event_start_timestamp, event_end_timestamp)

        # check if there is the path
        if not os.path.exists(constants.DATA_V3_PATH):
            os.makedirs(constants.DATA_V3_PATH)

        # save the data to Uniswap V3 directory
        df_mints.to_csv(
            f"{constants.DATA_V3_PATH}/{event_info[0]}_mints.csv", index=False
        )


if __name__ == "__main__":
    fetch_main()
