"""
Functions to fetch data from Uniswap V2.
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


def _fetch_batch_zero_v2(start_timestamp_gt: int) -> str:
    """
    Function to fetch the first 1000 swaps as the initial batch 0
    ordered by timestamp in ascending order.
    """

    # Start from fetching the first 1000 swaps as the initial batch 0
    # ordered by timestamp in ascending order
    params_start_gt = {"start_timestamp_gt": start_timestamp_gt - 1}

    swaps_0 = subgraph.run_query_var(
        constants.HTTP_V2, constants.QUERY_SWAP_V2, params_start_gt
    )

    return swaps_0


def _unwrap_df(df_all_swaps: pd.DataFrame, nested_list: list[str]) -> pd.DataFrame:
    """
    Function to unwrap the nested data.
    """

    # Unwrap the nested data level 1
    for nested in nested_list:
        # get the key of the nested dictionary
        nested_keys = df_all_swaps[nested][0].keys()

        # unwrap the nested dictionary
        for nested_key in nested_keys:
            df_all_swaps[f"{nested}_{nested_key}"] = df_all_swaps[nested].apply(
                lambda x: x[nested_key]
            )

        # drop the nested dictionary
        df_all_swaps = df_all_swaps.drop(nested, axis=1)

    return df_all_swaps


def fetch_swaps_v2(start_timestamp_gt: int, end_timestamp_lt: int) -> pd.DataFrame:
    """
    Function to fetch swaps from Uniswap V2.
    """

    # fetch the first 1000 swaps as the initial batch 0
    df_swaps_0 = _fetch_batch_zero_v2(start_timestamp_gt)

    # create a dataframe from the initial batch 0
    df_all_swaps = pd.DataFrame.from_dict(df_swaps_0["data"]["swaps"])

    # iterate through the rest of the batches and start from the last timestamp
    # which is got by batch 0
    iter_count = 0
    swaps_iter = df_swaps_0["data"]["swaps"]

    while int(swaps_iter[-1]["timestamp"]) < end_timestamp_lt:
        # get the last timestamp of the previous batch
        last_timestamp = int(swaps_iter[-1]["timestamp"])

        # create the query parameters
        params_last_timestamp = {"start_timestamp_gt": last_timestamp}

        # run the query
        result_iter = subgraph.run_query_var(
            constants.HTTP_V2, constants.QUERY_SWAP_V2, params_last_timestamp
        )

        # check if the result is empty
        if list(result_iter.keys()) == ["data"]:
            # list of swaps for this batch
            swaps_iter = result_iter["data"]["swaps"]

            # add list of this batch to the dataframe
            df_all_swaps = df_all_swaps.append(swaps_iter, ignore_index=True)

            # summarize the iteration count
            iter_count += 1
            print(
                f"Iteration count: {iter_count} last timestamp: {pd.to_datetime(last_timestamp, unit='s')}"
            )

    # drop the entries with timestamp larger than the end timestamp
    df_all_swaps = df_all_swaps[
        df_all_swaps["timestamp"].astype(int) < end_timestamp_lt
    ]

    # unwrap the nested data
    df_all_swaps = _unwrap_df(
        df_all_swaps, ["pair", "pair_token0", "pair_token1", "transaction"]
    )

    return df_all_swaps


if __name__ == "__main__":
    # test the function
    print(_timestamp_converter(constants.EVENT_ONE[1]))
    # print(
    #     pd.DataFrame.from_dict(
    #         _fetch_batch_zero_v2(_timestamp_converter(constants.EVENT_ONE))
    #     )
    # )
    # print(fetch_swaps_v2(_timestamp_converter(constants.EVENT_ONE), 0))
    # pd.DataFrame.from_dict(
    #     _fetch_batch_zero_v2(_timestamp_converter(constants.EVENT_ONE[1]))["data"]["swaps"]
    # ).to_csv(f"{constants.TEST_PATH}/test_swaps_v2.csv", index=False)

    # _unwrap_json(
    #     pd.DataFrame.from_dict(
    #         _fetch_batch_zero_v2(_timestamp_converter(constants.EVENT_ONE[1]))["data"][
    #             "swaps"
    #         ]
    #     ),
    #     ["pair", "pair_token0", "pair_token1", "transaction"],
    # ).to_csv(f"{constants.TEST_PATH}/test_swaps_v2.csv", index=False)
    pass
