"""
Function to aggregate data from multiple sources.
"""

import warnings
import os
import pandas as pd
from config import constants

# ignore warnings
warnings.filterwarnings("ignore")


def _swaps_v2_converter(df_swaps: pd.DataFrame, event_info: list[str]) -> pd.DataFrame:
    """
    Function to standardize the swaps data from v2.
    """

    # create a new column for the method name and event name
    df_swaps["dex"] = "v2"
    df_swaps["method"] = "swap"
    df_swaps["event_name"] = event_info[0]
    df_swaps["event_time"] = event_info[1]

    # convert the timestamp to datetime
    df_swaps["timestamp"] = pd.to_datetime(df_swaps["timestamp"], unit="s")

    # only keep the necessary columns
    df_swaps = df_swaps[
        [
            "dex",
            "method",
            "event_name",
            "event_time",
            "id",
            "timestamp",
            "pair_id",
            "pair_token0_id",
            "pair_token0_name",
            "pair_token0_symbol",
            "pair_token1_id",
            "pair_token1_name",
            "pair_token1_symbol",
            "amount0In",
            "amount0Out",
            "amount1In",
            "amount1Out",
            "amountUSD",
            "pair_reserve0",
            "pair_reserve1",
        ]
    ]

    # create two column for the amount0 and amount1
    # from the investors perspective
    df_swaps["txn_amount0"] = df_swaps["amount0Out"] - df_swaps["amount0In"]
    df_swaps["txn_amount1"] = df_swaps["amount1Out"] - df_swaps["amount1In"]

    df_swaps["token0_dollar_price"] = df_swaps["amountUSD"] / abs(
        df_swaps["txn_amount0"]
    )
    df_swaps["token1_dollar_price"] = df_swaps["amountUSD"] / abs(
        df_swaps["txn_amount1"]
    )

    df_swaps["pool_liquidity"] = (
        df_swaps["pair_reserve0"] * df_swaps["token0_dollar_price"]
        + df_swaps["pair_reserve1"] * df_swaps["token1_dollar_price"]
    )

    # rename the columns
    df_swaps = df_swaps.rename(
        columns={
            "pair_token0_id": "token0_id",
            "pair_token0_name": "token0_name",
            "pair_token0_symbol": "token0_symbol",
            "pair_token1_id": "token1_id",
            "pair_token1_name": "token1_name",
            "pair_token1_symbol": "token1_symbol",
            "pair_reserve0": "pool_amount0",
            "pair_reserve1": "pool_amount1",
        }
    )

    # drop the columns that are not needed
    df_swaps = df_swaps.drop(
        [
            "amount0In",
            "amount0Out",
            "amount1In",
            "amount1Out",
            "token0_dollar_price",
            "token1_dollar_price",
        ],
        axis=1,
    )

    # save the data to test
    df_swaps.to_csv(f"{constants.TEST_PATH}/swaps.csv", index=False)

    return df_swaps


def _swaps_v3_converter(df_swaps: pd.DataFrame, event_info: list[str]) -> pd.DataFrame:
    """
    Function to standardize the swaps data from v3.
    """

    # create a new column for the method name and event name
    df_swaps["dex"] = "v3"
    df_swaps["method"] = "swap"
    df_swaps["event_name"] = event_info[0]
    df_swaps["event_time"] = event_info[1]

    # convert the timestamp to datetime
    df_swaps["timestamp"] = pd.to_datetime(df_swaps["timestamp"], unit="s")

    # only keep the necessary columns
    df_swaps = df_swaps[
        [
            "dex",
            "method",
            "event_name",
            "event_time",
            "id",
            "timestamp",
            "pool_id",
            "token0_id",
            "token0_name",
            "token0_symbol",
            "token1_id",
            "token1_name",
            "token1_symbol",
            "amount0",
            "amount1",
            "amountUSD",
            "pool_totalValueLockedToken0",
            "pool_totalValueLockedToken1",
        ]
    ]

    # create two column for the amount0 and amount1
    # from the investors perspective
    df_swaps["txn_amount0"] = -df_swaps["amount0"]
    df_swaps["txn_amount1"] = -df_swaps["amount1"]

    df_swaps["token0_dollar_price"] = df_swaps["amountUSD"] / abs(
        df_swaps["txn_amount0"]
    )
    df_swaps["token1_dollar_price"] = df_swaps["amountUSD"] / abs(
        df_swaps["txn_amount1"]
    )

    df_swaps["pool_liquidity"] = (
        df_swaps["pool_totalValueLockedToken0"] * df_swaps["token0_dollar_price"]
        + df_swaps["pool_totalValueLockedToken1"] * df_swaps["token1_dollar_price"]
    )

    # drop the columns that are not needed
    df_swaps = df_swaps.drop(
        ["amount0", "amount1", "token0_dollar_price", "token1_dollar_price"], axis=1
    )

    # rename the columns
    df_swaps = df_swaps.rename(
        columns={
            "pool_id": "pair_id",
            "pool_totalValueLockedToken0": "pool_amount0",
            "pool_totalValueLockedToken1": "pool_amount1",
        }
    )

    # save the data to test
    df_swaps.to_csv(f"{constants.TEST_PATH}/swaps.csv", index=False)

    return df_swaps


def _burns_v2_converter(df_burns: pd.DataFrame, event_info: list[str]) -> pd.DataFrame:
    """
    Function to standardize the burns data from v2.
    """

    # create a new column for the method name and event name
    df_burns["dex"] = "v2"
    df_burns["method"] = "burn"
    df_burns["event_name"] = event_info[0]
    df_burns["event_time"] = event_info[1]

    # convert the timestamp to datetime
    df_burns["timestamp"] = pd.to_datetime(df_burns["timestamp"], unit="s")

    # only keep the necessary columns
    df_burns = df_burns[
        [
            "dex",
            "method",
            "event_name",
            "event_time",
            "id",
            "timestamp",
            "pair_id",
            "pair_token0_id",
            "pair_token0_name",
            "pair_token0_symbol",
            "pair_token1_id",
            "pair_token1_name",
            "pair_token1_symbol",
            "amount0",
            "amount1",
            "amountUSD",
            "pair_reserve0",
            "pair_reserve1",
        ]
    ]

    # from the investors perspective
    df_burns["txn_amount0"] = -df_burns["amount0"]
    df_burns["txn_amount1"] = -df_burns["amount1"]

    df_burns["token0_dollar_price"] = (
        df_burns["amountUSD"] / abs(df_burns["txn_amount0"]) / 2
    )

    df_burns["token1_dollar_price"] = (
        df_burns["amountUSD"] / abs(df_burns["txn_amount1"]) / 2
    )

    df_burns["pool_liquidity"] = (
        df_burns["pair_reserve0"] * df_burns["token0_dollar_price"]
        + df_burns["pair_reserve1"] * df_burns["token1_dollar_price"]
    )

    # rename the columns
    df_burns = df_burns.rename(
        columns={
            "pair_token0_id": "token0_id",
            "pair_token0_name": "token0_name",
            "pair_token0_symbol": "token0_symbol",
            "pair_token1_id": "token1_id",
            "pair_token1_name": "token1_name",
            "pair_token1_symbol": "token1_symbol",
            "pair_reserve0": "pool_amount0",
            "pair_reserve1": "pool_amount1",
        }
    )

    # drop the columns that are not needed
    df_burns = df_burns.drop(
        [
            "amount0",
            "amount1",
            "token0_dollar_price",
            "token1_dollar_price",
        ],
        axis=1,
    )

    # save the data to test
    df_burns.to_csv(f"{constants.TEST_PATH}/burns.csv", index=False)

    return df_burns


def _burns_v3_converter(df_burns: pd.DataFrame, event_info: list[str]) -> pd.DataFrame:
    """
    Function to standardize the burns data from v3.
    """

    # create a new column for the method name and event name
    df_burns["dex"] = "v3"
    df_burns["method"] = "burn"
    df_burns["event_name"] = event_info[0]
    df_burns["event_time"] = event_info[1]

    # convert the timestamp to datetime
    df_burns["timestamp"] = pd.to_datetime(df_burns["timestamp"], unit="s")

    # only keep the necessary columns
    df_burns = df_burns[
        [
            "dex",
            "method",
            "event_name",
            "event_time",
            "id",
            "timestamp",
            "pool_id",
            "token0_id",
            "token0_name",
            "token0_symbol",
            "token1_id",
            "token1_name",
            "token1_symbol",
            "amount0",
            "amount1",
            "amountUSD",
            "pool_totalValueLockedToken0",
            "pool_totalValueLockedToken1",
            "pool_token0Price",
            "pool_token1Price",
        ]
    ]

    # from the investors perspective
    df_burns["txn_amount0"] = -df_burns["amount0"]
    df_burns["txn_amount1"] = -df_burns["amount1"]

    # calculate the token prices
    df_burns["token0_dollar_price"] = df_burns["amountUSD"] / (
        abs(df_burns["txn_amount0"])
        + abs(df_burns["txn_amount1"]) / df_burns["pool_token1Price"]
    )

    df_burns["token1_dollar_price"] = df_burns["amountUSD"] / (
        abs(df_burns["txn_amount1"])
        + abs(df_burns["txn_amount0"]) / df_burns["pool_token0Price"]
    )

    # calculate the pool liquidity
    df_burns["pool_liquidity"] = (
        df_burns["pool_totalValueLockedToken0"] * df_burns["token0_dollar_price"]
        + df_burns["pool_totalValueLockedToken1"] * df_burns["token1_dollar_price"]
    )

    # rename the columns
    df_burns = df_burns.rename(
        columns={
            "pool_id": "pair_id",
            "pool_totalValueLockedToken0": "pool_amount0",
            "pool_totalValueLockedToken1": "pool_amount1",
        }
    )

    # drop the columns that are not needed
    df_burns = df_burns.drop(
        [
            "amount0",
            "amount1",
            "pool_token0Price",
            "pool_token1Price",
            "token0_dollar_price",
            "token1_dollar_price",
        ],
        axis=1,
    )

    # save the data to test
    df_burns.to_csv(f"{constants.TEST_PATH}/burns.csv", index=False)

    return df_burns


def _mints_v2_converter(df_mints: pd.DataFrame, event_info: list[str]) -> pd.DataFrame:
    """
    Function to standardize the mints data from v2.
    """

    # create a new column for the method name and event name
    df_mints["dex"] = "v2"
    df_mints["method"] = "mint"
    df_mints["event_name"] = event_info[0]
    df_mints["event_time"] = event_info[1]

    # convert the timestamp to datetime
    df_mints["timestamp"] = pd.to_datetime(df_mints["timestamp"], unit="s")

    # only keep the necessary columns
    df_mints = df_mints[
        [
            "dex",
            "method",
            "event_name",
            "event_time",
            "id",
            "timestamp",
            "pair_id",
            "pair_token0_id",
            "pair_token0_name",
            "pair_token0_symbol",
            "pair_token1_id",
            "pair_token1_name",
            "pair_token1_symbol",
            "amount0",
            "amount1",
            "amountUSD",
            "pair_reserve0",
            "pair_reserve1",
        ]
    ]

    # from the investors perspective
    df_mints["txn_amount0"] = df_mints["amount0"]
    df_mints["txn_amount1"] = df_mints["amount1"]

    df_mints["token0_dollar_price"] = (
        df_mints["amountUSD"] / abs(df_mints["txn_amount0"]) / 2
    )

    df_mints["token1_dollar_price"] = (
        df_mints["amountUSD"] / abs(df_mints["txn_amount1"]) / 2
    )

    df_mints["pool_liquidity"] = (
        df_mints["pair_reserve0"] * df_mints["token0_dollar_price"]
        + df_mints["pair_reserve1"] * df_mints["token1_dollar_price"]
    )

    # rename the columns
    df_mints = df_mints.rename(
        columns={
            "pair_token0_id": "token0_id",
            "pair_token0_name": "token0_name",
            "pair_token0_symbol": "token0_symbol",
            "pair_token1_id": "token1_id",
            "pair_token1_name": "token1_name",
            "pair_token1_symbol": "token1_symbol",
            "pair_reserve0": "pool_amount0",
            "pair_reserve1": "pool_amount1",
        }
    )

    # drop the columns that are not needed
    df_mints = df_mints.drop(
        [
            "amount0",
            "amount1",
            "token0_dollar_price",
            "token1_dollar_price",
        ],
        axis=1,
    )

    # save the data to test
    df_mints.to_csv(f"{constants.TEST_PATH}/mints.csv", index=False)

    return df_mints


def _mints_v3_converter(df_mints: pd.DataFrame, event_info: list[str]) -> pd.DataFrame:
    """
    Function to standardize the mint data from v3.
    """

    # create a new column for the method name and event name
    df_mints["dex"] = "v3"
    df_mints["method"] = "mint"
    df_mints["event_name"] = event_info[0]
    df_mints["event_time"] = event_info[1]

    # convert the timestamp to datetime
    df_mints["timestamp"] = pd.to_datetime(df_mints["timestamp"], unit="s")

    # only keep the necessary columns
    df_mints = df_mints[
        [
            "dex",
            "method",
            "event_name",
            "event_time",
            "id",
            "timestamp",
            "pool_id",
            "token0_id",
            "token0_name",
            "token0_symbol",
            "token1_id",
            "token1_name",
            "token1_symbol",
            "amount0",
            "amount1",
            "amountUSD",
            "pool_totalValueLockedToken0",
            "pool_totalValueLockedToken1",
            "pool_token0Price",
            "pool_token1Price",
        ]
    ]

    # from the investors perspective
    df_mints["txn_amount0"] = df_mints["amount0"]
    df_mints["txn_amount1"] = df_mints["amount1"]

    # calculate the token prices
    df_mints["token0_dollar_price"] = df_mints["amountUSD"] / (
        abs(df_mints["txn_amount0"])
        + abs(df_mints["txn_amount1"]) / df_mints["pool_token1Price"]
    )

    df_mints["token1_dollar_price"] = df_mints["amountUSD"] / (
        abs(df_mints["txn_amount1"])
        + abs(df_mints["txn_amount0"]) / df_mints["pool_token0Price"]
    )

    # calculate the pool liquidity
    df_mints["pool_liquidity"] = (
        df_mints["pool_totalValueLockedToken0"] * df_mints["token0_dollar_price"]
        + df_mints["pool_totalValueLockedToken1"] * df_mints["token1_dollar_price"]
    )

    # rename the columns
    df_mints = df_mints.rename(
        columns={
            "pool_id": "pair_id",
            "pool_totalValueLockedToken0": "pool_amount0",
            "pool_totalValueLockedToken1": "pool_amount1",
        }
    )

    # drop the columns that are not needed
    df_mints = df_mints.drop(
        [
            "amount0",
            "amount1",
            "pool_token0Price",
            "pool_token1Price",
            "token0_dollar_price",
            "token1_dollar_price",
        ],
        axis=1,
    )

    # save the data to test
    df_mints.to_csv(f"{constants.TEST_PATH}/mints.csv", index=False)

    return df_mints


def generate_panel() -> None:
    """
    Function to aggregate data from multiple sources.
    """

    # check if there is the path WORKING_DATA_PATH
    if not os.path.exists(constants.WORKING_DATA_PATH):
        os.makedirs(constants.WORKING_DATA_PATH)

    # create a list for the panel data
    panel_data = []

    for data_cat in ["swaps", "burns", "mints"]:
        for event_info in [
            constants.EVENT_ONE,
            constants.EVENT_TWO,
            constants.EVENT_THREE,
            constants.EVENT_FOUR,
        ]:
            # read the data
            df_v2 = pd.read_csv(
                f"{constants.DATA_V2_PATH}/{event_info[0]}_{data_cat}.csv"
            )
            df_v3 = pd.read_csv(
                f"{constants.DATA_V3_PATH}/{event_info[0]}_{data_cat}.csv"
            )

            # convert the data
            if data_cat == "swaps":
                df_v2 = _swaps_v2_converter(df_v2, event_info)
                df_v3 = _swaps_v3_converter(df_v3, event_info)
            elif data_cat == "burns":
                df_v2 = _burns_v2_converter(df_v2, event_info)
                df_v3 = _burns_v3_converter(df_v3, event_info)
            elif data_cat == "mints":
                df_v2 = _mints_v2_converter(df_v2, event_info)
                df_v3 = _mints_v3_converter(df_v3, event_info)

            # append the data
            panel_data.append(df_v2)
            panel_data.append(df_v3)

    # concatenate the data
    df_panel = pd.concat(panel_data)

    # save the data
    df_panel.to_csv(f"{constants.WORKING_DATA_PATH}/panel.csv", index=False)


if __name__ == "__main__":
    # test the function
    print(
        _swaps_v2_converter(
            pd.read_csv(f"{constants.DATA_V2_PATH}/{constants.EVENT_ONE[0]}_swaps.csv"),
            constants.EVENT_ONE,
        )
    )

    # test the function for v3
    print(
        _swaps_v3_converter(
            pd.read_csv(f"{constants.DATA_V3_PATH}/{constants.EVENT_ONE[0]}_swaps.csv"),
            constants.EVENT_ONE,
        )
    )

    # test the function for burns
    print(
        _burns_v2_converter(
            pd.read_csv(f"{constants.DATA_V2_PATH}/{constants.EVENT_ONE[0]}_burns.csv"),
            constants.EVENT_ONE,
        )
    )

    # test the function for burns
    print(
        _burns_v3_converter(
            pd.read_csv(f"{constants.DATA_V3_PATH}/{constants.EVENT_ONE[0]}_burns.csv"),
            constants.EVENT_ONE,
        )
    )

    # test the function for mints
    print(
        _mints_v2_converter(
            pd.read_csv(f"{constants.DATA_V2_PATH}/{constants.EVENT_ONE[0]}_mints.csv"),
            constants.EVENT_ONE,
        )
    )
