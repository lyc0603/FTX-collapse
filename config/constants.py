"""
Global constants
"""

from os import path
from config.settings import PROJECT_ROOT

# Path to the directory containing the project's source code
RAW_DATA_PATH = path.join(PROJECT_ROOT, "raw_data")
WORKING_DATA_PATH = path.join(PROJECT_ROOT, "working_data")
ENVIRON_PATH = path.join(PROJECT_ROOT, "environ")
TEST_PATH = path.join(PROJECT_ROOT, "test")
DATA_V2_PATH = path.join(RAW_DATA_PATH, "uniswap_v2")
DATA_V3_PATH = path.join(RAW_DATA_PATH, "uniswap_v3")

# Event timestring UTC
# 币安宣布并购FTX以救济同行(随后FTX的平台币FTX Token开始暴跌). FTX平台出现挤兑.
EVENT_ONE = ("event_one", "2022-11-06 15:47:00")
# 赵长鹏考虑收购FTX
EVENT_TWO = ("event_two", "2022-11-08 16:09:00")
# 赵长鹏写给币安投资者的信
EVENT_THREE = ("event_three", "2022-11-09 14:30:00")
# 币安宣布放弃并表示问题太大，无法解决，随后FTX申请破产
EVENT_FOUR = ("event_four", "2022-11-09 21:00:00")

# Event window in hours
EVENT_WINDOW = 2

# API HTTP
HTTP_V2 = "https://api.thegraph.com/subgraphs/name/ianlapham/uniswapv2"
HTTP_V3 = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"

# Query Scripts
QUERY_SWAP_V2 = """
query ($start_timestamp_gt: Int!){
  swaps(
    first: 1000
    orderBy: timestamp
    orderDirection: asc
    where: {timestamp_gt: $start_timestamp_gt}
  ) {
    amount0In
    amount0Out
    amount1In
    amount1Out
    amountUSD
    from
    id
    logIndex
    pair {
      createdAtBlockNumber
      createdAtTimestamp
      id
      liquidityProviderCount
      reserve0
      reserve1
      reserveETH
      reserveUSD
      token0Price
      token1Price
      totalSupply
      trackedReserveETH
      txCount
      untrackedVolumeUSD
      volumeToken0
      volumeToken1
      volumeUSD
      token0 {
        decimals
        derivedETH
        id
        name
        symbol
        totalLiquidity
        totalSupply
        tradeVolume
        tradeVolumeUSD
        txCount
        untrackedVolumeUSD
      }
      token1 {
        decimals
        derivedETH
        id
        name
        symbol
        totalLiquidity
        totalSupply
        tradeVolume
        tradeVolumeUSD
        txCount
        untrackedVolumeUSD
      }
    }
    sender
    timestamp
    to
    transaction {
      blockNumber
      id
      timestamp
    }
  }
}
"""

QUERY_SWAP_V3 = """
query ($start_timestamp_gt: Int!){
  swaps(
    first: 1000
    orderBy: timestamp
    orderDirection: asc
    where: {timestamp_gt: $start_timestamp_gt}
  ) {
    amount0
    amount1
    amountUSD
    id
    logIndex
    origin
    pool {
      collectedFeesToken0
      collectedFeesToken1
      collectedFeesUSD
      createdAtBlockNumber
      createdAtTimestamp
      feeGrowthGlobal0X128
      feeGrowthGlobal1X128
      feeTier
      feesUSD
      id
      liquidity
      liquidityProviderCount
      observationIndex
      sqrtPrice
      tick
      token0Price
      token1Price
      totalValueLockedETH
      totalValueLockedToken0
      totalValueLockedToken1
      totalValueLockedUSD
      totalValueLockedUSDUntracked
      txCount
      untrackedVolumeUSD
      volumeToken0
      volumeToken1
      volumeUSD
    }
    recipient
    sender
    sqrtPriceX96
    tick
    timestamp
    token0 {
      decimals
      derivedETH
      feesUSD
      id
      name
      poolCount
      symbol
      totalSupply
      totalValueLocked
      totalValueLockedUSD
      totalValueLockedUSDUntracked
      txCount
      untrackedVolumeUSD
      volume
      volumeUSD
    }
    token1 {
      decimals
      derivedETH
      feesUSD
      id
      name
      poolCount
      symbol
      totalSupply
      totalValueLocked
      totalValueLockedUSD
      totalValueLockedUSDUntracked
      txCount
      untrackedVolumeUSD
      volume
      volumeUSD
    }
    transaction {
      blockNumber
      gasPrice
      gasUsed
      id
      timestamp
    }
  }
}
"""

QUERY_BURN_V2 = """
query ($start_timestamp_gt: Int!){
  burns(
    first: 1000
    orderBy: timestamp
    orderDirection: asc
    where: {timestamp_gt: $start_timestamp_gt}
  ) {
    amount0
    amount1
    amountUSD
    feeLiquidity
    feeTo
    id
    liquidity
    logIndex
    needsComplete
    sender
    timestamp
    to
    pair {
      createdAtBlockNumber
      createdAtTimestamp
      id
      liquidityProviderCount
      reserve0
      reserve1
      reserveETH
      reserveUSD
      token0Price
      token1Price
      totalSupply
      trackedReserveETH
      txCount
      untrackedVolumeUSD
      volumeToken0
      volumeToken1
      volumeUSD
      token0 {
        decimals
        derivedETH
        id
        name
        symbol
        totalLiquidity
        totalSupply
        tradeVolume
        tradeVolumeUSD
        txCount
        untrackedVolumeUSD
      }
      token1 {
        decimals
        derivedETH
        id
        name
        symbol
        totalLiquidity
        totalSupply
        tradeVolume
        tradeVolumeUSD
        txCount
        untrackedVolumeUSD
      }
    }
    transaction {
      blockNumber
      id
      timestamp
    }
  }
}
"""

QUERY_BURN_V3 = """
query ($start_timestamp_gt: Int!){
  burns(
    first: 1000
    orderBy: timestamp
    orderDirection: asc
    where: {timestamp_gt: $start_timestamp_gt}
  ) {
    amount
    amount0
    amount1
    amountUSD
    id
    logIndex
    origin
    owner
    pool {
      collectedFeesToken0
      collectedFeesToken1
      collectedFeesUSD
      createdAtBlockNumber
      createdAtTimestamp
      feeGrowthGlobal0X128
      feeGrowthGlobal1X128
      feeTier
      feesUSD
      id
      liquidity
      liquidityProviderCount
      observationIndex
      sqrtPrice
      tick
      token0Price
      token1Price
      totalValueLockedETH
      totalValueLockedToken0
      totalValueLockedToken1
      totalValueLockedUSD
      totalValueLockedUSDUntracked
      txCount
      untrackedVolumeUSD
      volumeToken0
      volumeToken1
      volumeUSD
    }
    tickLower
    tickUpper
    timestamp
    token0 {
      decimals
      derivedETH
      feesUSD
      id
      name
      poolCount
      symbol
      totalSupply
      totalValueLocked
      totalValueLockedUSD
      totalValueLockedUSDUntracked
      txCount
      untrackedVolumeUSD
      volume
      volumeUSD
    }
    token1 {
      decimals
      derivedETH
      feesUSD
      id
      name
      poolCount
      symbol
      totalSupply
      totalValueLocked
      totalValueLockedUSD
      totalValueLockedUSDUntracked
      txCount
      untrackedVolumeUSD
      volume
      volumeUSD
    }
    transaction {
      blockNumber
      gasPrice
      gasUsed
      id
      timestamp
    }
  }
}
"""

QUERY_MINT_V2 = """
query ($start_timestamp_gt: Int!){
  mints(
    first: 1000
    orderBy: timestamp
    orderDirection: asc
    where: {timestamp_gt: $start_timestamp_gt}
  ) {
    amount0
    amount1
    amountUSD
    feeLiquidity
    feeTo
    id
    liquidity
    logIndex
    pair {
      createdAtBlockNumber
      createdAtTimestamp
      id
      liquidityProviderCount
      reserve0
      reserve1
      reserveETH
      reserveUSD
      token0 {
        decimals
        derivedETH
        id
        name
        symbol
        totalLiquidity
        totalSupply
        tradeVolume
        tradeVolumeUSD
        txCount
        untrackedVolumeUSD
      }
      token0Price
      token1 {
        decimals
        derivedETH
        id
        name
        symbol
        totalLiquidity
        totalSupply
        tradeVolume
        tradeVolumeUSD
        txCount
        untrackedVolumeUSD
      }
      token1Price
      totalSupply
      trackedReserveETH
      txCount
      untrackedVolumeUSD
      volumeToken0
      volumeToken1
      volumeUSD
    }
    sender
    timestamp
    to
    transaction {
      blockNumber
      id
      timestamp
    }
  }
}
"""

QUERY_MINT_V3 = """
query ($start_timestamp_gt: Int!){
  mints(
    first: 1000
    orderBy: timestamp
    orderDirection: asc
    where: {timestamp_gt: $start_timestamp_gt}
  ) {
    amount
    amount0
    amount1
    amountUSD
    id
    logIndex
    origin
    owner
    pool {
      collectedFeesToken0
      collectedFeesToken1
      collectedFeesUSD
      createdAtBlockNumber
      createdAtTimestamp
      feeGrowthGlobal0X128
      feeGrowthGlobal1X128
      feeTier
      feesUSD
      id
      liquidity
      liquidityProviderCount
      observationIndex
      sqrtPrice
      tick
      token0Price
      token1Price
      totalValueLockedETH
      totalValueLockedToken0
      totalValueLockedToken1
      totalValueLockedUSD
      totalValueLockedUSDUntracked
      txCount
      untrackedVolumeUSD
      volumeToken0
      volumeToken1
      volumeUSD
    }
    sender
    tickLower
    tickUpper
    timestamp
    token0 {
      decimals
      derivedETH
      feesUSD
      id
      name
      poolCount
      symbol
      totalSupply
      totalValueLocked
      totalValueLockedUSD
      totalValueLockedUSDUntracked
      txCount
      untrackedVolumeUSD
      volume
      volumeUSD
    }
    token1 {
      decimals
      derivedETH
      feesUSD
      id
      name
      poolCount
      symbol
      totalSupply
      totalValueLocked
      totalValueLockedUSD
      totalValueLockedUSDUntracked
      txCount
      untrackedVolumeUSD
      volume
      volumeUSD
    }
    transaction {
      blockNumber
      gasPrice
      gasUsed
      id
      timestamp
    }
  }
}
"""
