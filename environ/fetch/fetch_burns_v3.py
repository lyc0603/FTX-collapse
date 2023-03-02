"""
Functions to fetch burns data from Uniswap V3.
"""
import warnings
import pandas as pd
import environ.fetch.subgraph_query as subgraph
from config import constants

# ignore warnings
warnings.filterwarnings("ignore")


def _timestamp_converter(datestr: str) -> int:
    """
    Function to convert date string to unix timestamp.
    """

    # Convert date string to unix timestamp
    timestamp = pd.to_datetime(datestr).timestamp()

    return int(timestamp)


def _fetch_batch_zero_v3(start_timestamp_gt: int) -> str:
    """
    Function to fetch the first 1000 burns as the initial batch 0
    ordered by timestamp in ascending order.
    """

    # Start from fetching the first 1000 burns as the initial batch 0
    # ordered by timestamp in ascending order
    params_start_gt = {"start_timestamp_gt": start_timestamp_gt - 1}

    burns_0 = subgraph.run_query_var(
        constants.HTTP_V3, constants.QUERY_BURN_V3, params_start_gt
    )

    return burns_0


def _unwrap_df(df_all_burns: pd.DataFrame, nested_list: list[str]) -> pd.DataFrame:
    """
    Function to unwrap the nested data.
    """

    # Unwrap the nested data level 1
    for nested in nested_list:
        # get the key of the nested dictionary
        nested_keys = df_all_burns[nested][0].keys()

        # unwrap the nested dictionary
        for nested_key in nested_keys:
            df_all_burns[f"{nested}_{nested_key}"] = df_all_burns[nested].apply(
                lambda x: x[nested_key]
            )

        # drop the nested dictionary
        df_all_burns = df_all_burns.drop(nested, axis=1)

    return df_all_burns


def fetch_burns_v3(start_timestamp_gt: int, end_timestamp_lt: int) -> pd.DataFrame:
    """
    Function to fetch burns from Uniswap V3.
    """

    # fetch the first 1000 burns as the initial batch 0
    df_burns_0 = _fetch_batch_zero_v3(start_timestamp_gt)

    # create a dataframe from the initial batch 0
    df_all_burns = pd.DataFrame.from_dict(df_burns_0["data"]["burns"])

    # iterate through the rest of the batches and start from the last timestamp
    # which is got by batch 0
    iter_count = 0
    burns_iter = df_burns_0["data"]["burns"]

    while int(burns_iter[-1]["timestamp"]) < end_timestamp_lt:
        # get the last timestamp of the previous batch
        last_timestamp = int(burns_iter[-1]["timestamp"])

        # create the query parameters
        params_last_timestamp = {"start_timestamp_gt": last_timestamp}

        # run the query
        result_iter = subgraph.run_query_var(
            constants.HTTP_V3, constants.QUERY_BURN_V3, params_last_timestamp
        )

        # check if the result is empty
        if list(result_iter.keys()) == ["data"]:
            # list of burns for this batch
            burns_iter = result_iter["data"]["burns"]

            # add list of this batch to the dataframe
            df_all_burns = df_all_burns.append(burns_iter, ignore_index=True)

            # summarize the iteration count
            iter_count += 1
            print(
                f"Iteration count: {iter_count} last timestamp: {pd.to_datetime(last_timestamp, unit='s')}"
            )

    # drop the entries with timestamp larger than the end timestamp
    df_all_burns = df_all_burns[
        df_all_burns["timestamp"].astype(int) < end_timestamp_lt
    ]

    # unwrap the nested data
    df_all_burns = _unwrap_df(df_all_burns, ["pool", "token0", "token1", "transaction"])

    return df_all_burns


if __name__ == "__main__":
    # fetch burns from Uniswap V3
    df_burns_v3 = _fetch_batch_zero_v3(
        _timestamp_converter(constants.EVENT_ONE[1]),
    )

    # print the dataframe
    print(df_burns_v3)

    pass
