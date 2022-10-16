import argparse
from .collect_json_schema import collect_json_schema
from .collect_csv_tables import collect_csv_tables


def add_collect_json_schema_subparser(subparsers):
    parser = subparsers.add_parser('collect_json_schema')
    parser.add_argument('dataset_path', type=str, help='Path to json dataset')
    parser.add_argument('schema_path', type=str, help='Path to resulting tsv file')


def add_collect_csv_tables_subparser(subparsers):
    parser = subparsers.add_parser('collect_csv_tables')
    parser.add_argument('dataset_path', type=str, help='Path to json dataset')
    parser.add_argument('csv_tables_dir', type=str, help='Path to resulting csv tables dir')


def main():
    parser = argparse.ArgumentParser(prog='dataset_parsing')

    subparsers = parser.add_subparsers(dest='command')
    add_collect_json_schema_subparser(subparsers)
    add_collect_csv_tables_subparser(subparsers)
    args = parser.parse_args()

    if args.command == 'collect_json_schema':
        collect_json_schema(args.dataset_path, args.schema_path)
    elif args.command == 'collect_csv_tables':
        collect_csv_tables(args.dataset_path, args.csv_tables_dir)
    else:
        raise RuntimeError(f'Unexpected command {args.command}')


if __name__ == '__main__':
    main()
