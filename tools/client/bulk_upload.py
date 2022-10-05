import argparse
import json
import psycopg
import os

from contextlib import closing
from tqdm import tqdm

UPLOAD_CHUNK_SIZE = 8 * 1024 * 1024
SCHEMA_NAME = 'dataset'
TABLES = {
    'paper':   'paper.csv',
    'author':  'author.csv',
    'org':     'org.csv',
    'venue':   'venue.csv',
    'fos':     'fos_ids.csv',
    'keyword': 'keyword_ids.csv',

    'paper_author':    'paper_author.csv',
    'author_org':      'author_org.csv',
    'paper_venue':     'paper_venue.csv',
    'paper_reference': 'paper_reference.csv',
    'paper_fos':       'paper_fos.csv',
    'paper_keyword':   'paper_keyword.csv',
    'paper_url':       'paper_url.csv',
}


def check_all_csv_files_exists(csv_tables_path):
    for name, csv_fname in TABLES.items():
        csv_fpath = os.path.join(csv_tables_path, csv_fname)
        assert os.path.isfile(csv_fpath), f'Missing regular file: {csv_fpath}'


def create_connection(cfg_path):
    with open(cfg_path) as f:
        cfg = json.load(f)

    conn_str = ' '.join(f'{key}={value}' for key, value in cfg.items())
    return psycopg.connect(conn_str)


def upload_table(cursor, table_name, table_path):
    copy_query = psycopg.sql.SQL(
        f'COPY dataset.{table_name} FROM STDIN CSV HEADER'
        #"COPY {} FROM STDIN CSV HEADER").format(
        #psycopg.sql.Identifier(SCHEMA_NAME + '.' + table_name)
    )
    total_size = os.stat(table_path).st_size
    with open(table_path) as f, tqdm(total=total_size, desc=table_name, unit_scale=True) as pbar:
        chunk = f.read(UPLOAD_CHUNK_SIZE)
        with cursor.copy(copy_query) as copy:
            while chunk:
                copy.write(chunk)
                pbar.update(len(chunk))
                chunk = f.read(UPLOAD_CHUNK_SIZE)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_tables_path')
    parser.add_argument('db_cfg')
    args = parser.parse_args()

    check_all_csv_files_exists(args.csv_tables_path)

    with create_connection(args.db_cfg) as connection:
        with connection.cursor() as cursor:
            for table_name, csv_fname in TABLES.items():
                upload_table(cursor, table_name, os.path.join(args.csv_tables_path, csv_fname))
            connection.commit()


if __name__ == '__main__':
    main()
