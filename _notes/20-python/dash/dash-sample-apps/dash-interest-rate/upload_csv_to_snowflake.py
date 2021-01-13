import os
from textwrap import dedent

from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
import pandas as pd


def create_or_replace_table(connection, df, name):
    # Load the actual csv file

    # Create SQL columns based on the columns of that dataframe
    types = (
        df.dtypes.copy()
        .replace("float64", "FLOAT")
        .replace("int64", "INT")
        .replace("object", "STRING")
    )
    
    sql_cols = ",\n".join(types.index + " " + types.values)

    cmd = f"""
CREATE OR REPLACE TABLE {name} (
{sql_cols}   
)
    """

    # print(cmd)
    return connection.execute(cmd)


def load_data(path, table_name):
    print('-'*50)

    # Create Engine and connect to DB
    engine = create_engine(
        URL(
            account=FLAKE_ACCOUNT,
            user=FLAKE_USER,
            password=FLAKE_PW,
            database=flake_db,
            schema="public",
            warehouse=flake_warehouse,
            role="sysadmin",
        ),
        pool_size=5,
        pool_recycle=1800,
        pool_pre_ping=True,
    )

    print('connecting to snowflake database')
    connection = engine.connect()

    # Create Table
    print('create table {} in snowflake'.format(table_name))
    abs_path = os.path.abspath(path)
    df = pd.read_csv(abs_path, nrows=5)
    create_or_replace_table(connection, df, name=table_name)

    stage = "LOAN_STAGE_" + table_name
    print('creating stage {} in snowflake'.format(stage))
    # First remove all the content of the stage
    cmd = f"""create or replace stage {stage}
file_format = (type = 'CSV' field_delimiter = ',' skip_header = 1);
    """
    connection.execute(cmd)

    # Upload the CSV file
    cmd = f"""PUT file://{abs_path} @{stage} """
    connection.execute(cmd)

    print('uploading {} into table {} snowflake'.format(path, table_name))
    # Copy the CSV file into the table
    connection.execute(f"COPY INTO {table_name} FROM @{stage}")
    
    
if __name__ == "__main__":
    # os.environ["http_proxy"] = "http://web-proxy.rose.hp.com:8080"
    # os.environ["https_proxy"] = "http://web-proxy.rose.hp.com:8080"
    # Snowflake vars
    FLAKE_ACCOUNT = os.getenv("FLAKE_ACCOUNT")
    FLAKE_USER = os.getenv("FLAKE_USER")
    FLAKE_PW = os.getenv("FLAKE_PW")
    # print(FLAKE_ACCOUNT)
    # print(FLAKE_USER)
    # print(FLAKE_PW)

    flake_warehouse = "snowflake_demos"
    flake_db = "LOANS"


    load_data("data/loan_desc.csv", 'LOAN_DESC')
    load_data("data/clean_loan.csv", 'LOAN_CLEAN')
