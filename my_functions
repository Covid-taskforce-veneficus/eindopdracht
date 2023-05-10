def load_dataset():
    
    import os

    import pandas as pd
    from dotenv import load_dotenv
    from sqlalchemy import create_engine
    
    load_dotenv()

    DB_USER = os.environ["DB_USER"]
    DB_PASSWORD = os.environ["DB_PASSWORD"]
    DB_HOSTNAME = os.environ["DB_HOSTNAME"]
    DB_NAME = os.environ["DB_NAME"]

    print(f"If everything is set up correctly this will print the database name: {DB_NAME}")

    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:5432/{DB_NAME}")
    result = engine.execute("SELECT 1")
    result.first()

    # regendata
    df1 = pd.read_sql_query(
        """
    select *
    from
    covid."Rain_Data"
    """,
        con=engine,
    )

    # Orderdata

    df2 = pd.read_sql_query(
        """
    select *
    from covid."Orders_Rotterdam" om
    """,
        con=engine,
    )

    df1.rename(columns={"DATE": "date"}, inplace=True)
    df1["date"] = pd.to_datetime(df1["date"])
    df2["date"] = pd.to_datetime(df2["date"])

    df = pd.merge(df1, df2, on="date")
    df.drop(["index_x", "index_y"], axis=1, inplace=True)
    return df 
