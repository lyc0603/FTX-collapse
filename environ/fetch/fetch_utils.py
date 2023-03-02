"""
Utility functions for fetch module.
"""

import datetime
import pandas as pd
from config import constants


def timestamp_converter(datestr: str) -> dict[str, int]:
    """
    Function to convert date string to unix timestamp.
    """

    # Convert date string to unix timestamp
    start_timestamp = (
        pd.to_datetime(datestr) - datetime.timedelta(hours=constants.EVENT_WINDOW)
    ).timestamp()
    end_timestamp = (
        pd.to_datetime(datestr) + datetime.timedelta(hours=constants.EVENT_WINDOW)
    ).timestamp()

    return {
        "start_timestamp": int(start_timestamp),
        "end_timestamp": int(end_timestamp),
    }


if __name__ == "__main__":
    print(timestamp_converter(constants.EVENT_ONE[1]))
