import argparse
import json
import psycopg


def create_connection(cfg_path):
    with open(cfg_path) as f:
        cfg = json.load(f)

    conn_str = ' '.join(f'{key}={value}' for key, value in cfg.items())
    return psycopg.connect(conn_str)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('sql_file')
    parser.add_argument('db_cfg')
    args = parser.parse_args()

    with open(args.sql_file) as f:
        queries = f.read()

    with create_connection(args.db_cfg) as connection:
        with connection.cursor() as cursor:
            cursor.execute(queries)
            connection.commit()


if __name__ == '__main__':
    main()
