#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--data-file', required=True, help='Path to data file (parquet or csv)')
@click.option('--target-table', required=True, help='Target table name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading data')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, data_file, target_table, chunksize):
    """Ingest NYC taxi data into PostgreSQL database."""
    
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    print(f"Reading file: {data_file}")
    
    if data_file.endswith('.parquet'):
        df = pd.read_parquet(data_file)
        print(f"Loaded {len(df)} rows from parquet file")
        print(f"Columns: {df.columns.tolist()}")
        
        df.to_sql(
            name=target_table,
            con=engine,
            if_exists='replace',
            index=False,
            chunksize=chunksize
        )
        
    elif data_file.endswith('.csv'):
        df = pd.read_csv(data_file)
        print(f"Loaded {len(df)} rows from CSV file")
        print(f"Columns: {df.columns.tolist()}")
        
        df.to_sql(
            name=target_table,
            con=engine,
            if_exists='replace',
            index=False,
            chunksize=chunksize
        )
    else:
        raise ValueError("Unsupported file format. Use .parquet or .csv")
    
    print(f"✓ Data successfully written to table '{target_table}'")

if __name__ == '__main__':
    run()