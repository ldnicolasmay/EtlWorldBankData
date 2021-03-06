from typing import Dict
import pandas as pd

from worldbank_indicator_data import get_worldbank_indicator_dfs_dict
from iso_country_code_data import get_iso_country_code_df


def write_df_to_s3_parquet(
        df: pd.DataFrame,
        bucket_name: str,
        key_prefix: str,
        key_suffix: str
):
    """
    Simplifies writing DataFrame to S3 as parquet file

    :param df: DataFrame to write
    :param bucket_name: S3 bucket name
    :param key_prefix: S3 key prefix
    :param key_suffix: S3 key suffix
    """
    df.to_parquet(
        f"s3://{bucket_name}/{key_prefix}/{key_suffix}",
        index=False
    )


def main():
    """
    Driver method for the EtlWorldBankData app
    """

    # Get ISO country code data
    iso_country_code_df: pd.DataFrame = get_iso_country_code_df()
    print(f"Dimensions of iso_country_code_df: {iso_country_code_df.shape}")

    # Define World Bank indicator codes; Get World Bank indicator DataFrames in a dict
    worldbank_indicator_code_dict: Dict[str, str] = {
        "IT.NET.SECR": "Secure Internet servers",
        "IT.NET.SECR.P6": "Secure Internet servers (per 1 million people)",
        "IT.NET.USER.ZS": "Individuals using the Internet (% of population)",
        "MS.MIL.TOTL.P1": "Armed forces personnel, total",
        "MS.MIL.TOTL.TF.ZS": "Armed forces personnel (% of total labor force)",
        "MS.MIL.XPND.CN": "Military expenditure (current LCU)",
        "MS.MIL.XPND.GD.ZS": "Military expenditure (% of GDP)",
        "MS.MIL.XPND.ZS": "Military expenditure (% of central government expenditure)",
        "SP.POP.TOTL": "Population, total",
    }

    worldbank_indicator_dfs_dict: Dict[str, pd.DataFrame] = \
        get_worldbank_indicator_dfs_dict(worldbank_indicator_code_dict)

    for key, df in worldbank_indicator_dfs_dict.items():
        print(f"Dimensions of {key}: {df.shape}")
        write_df_to_s3_parquet(df, "udacity-ooni-project", "parquet/worldbank", f"{key}.parquet")


if __name__ == "__main__":
    main()
