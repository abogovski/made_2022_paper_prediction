import argparse
from contextlib import closing
import json
import psycopg
from .bulk_upload import upload_all_tables


def create_connection(cfg_file):
    with closing(cfg_file) as f:
        cfg = json.load(f)

    conn_str = ' '.join(f'{key}={value}' for key, value in cfg.items())
    return psycopg.connect(conn_str)


def add_apply_sql_parser(subparsers):
    parser = subparsers.add_parser(
        'apply_sql',
        help='Apply sql file to database',
    )
    parser.add_argument(
        'sql_file',
        help='Sql File',
        type=argparse.FileType('r'),
    )
    parser.add_argument(
        'database_config',
        help='Path to database connection config file',
        type=argparse.FileType('r'),
    )


def add_bulk_upload_parser(subparsers):
    parser = subparsers.add_parser(
        'bulk_upload',
        help='Bulk-upload csv tables to database',
    )
    parser.add_argument(
        'csv_tables',
        help='Path to csv_tables directory',
        type=str,
    )
    parser.add_argument(
        'database_config',
        help='Path to database connection config file',
        type=argparse.FileType('r'),
    )


def main():
    parser = argparse.ArgumentParser(prog='dbclient')
    subparsers = parser.add_subparsers(dest='command')
    add_apply_sql_parser(subparsers)
    add_bulk_upload_parser(subparsers)
    args = parser.parse_args()

    with create_connection(args.database_config) as connection:
        with connection.cursor() as cursor:
            if args.command == 'apply_sql':
                with closing(args.sql_file) as f:
                    queries = f.read()
                cursor.execute(queries)

            elif args.command == 'bulk_upload':
                upload_all_tables(cursor, args.csv_tables)

            else:
                raise RuntimeError(f'Unexpected command {args.command}')

        connection.commit()


if __name__ == '__main__':
    main()
