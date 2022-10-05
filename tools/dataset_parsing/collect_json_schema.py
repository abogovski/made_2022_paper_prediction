import argparse
from collections import defaultdict, deque, Counter

from dataset import read_dataset


def get_flat_field_types(obj):
    queue = deque([('', obj)])
    while queue:
        path, obj = queue.pop()
        if isinstance(obj, list):
            for value in obj:
                queue.append((path + '/<idx>', value))
        elif isinstance(obj, dict):
            if obj:
                for key, value in obj.items():
                    queue.append((path + '/' + key, value))
        else:
            yield path, type(obj)


def save_schema(path, schema):
    with open(path, 'w') as f:
        for key, counter in sorted(schema.items(), key=lambda kv: kv[0]):
            f.write(
                f'{key}\t' +
                ', '.join(
                    tp + ': ' + str(cnt)
                    for tp, cnt in sorted(counter.items(), key=lambda kv: -kv[1])
                ) + '\n'
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_path')
    parser.add_argument('schema_path')
    args = parser.parse_args()

    try:
        schema = defaultdict(Counter)
        for entry in read_dataset(args.dataset_path):
            for field_key, field_type in get_flat_field_types(entry):
                schema[field_key][field_type.__name__] += 1
    finally:
        save_schema(args.schema_path, schema)


if __name__ == '__main__':
    main()
