import csv
import os


class MultiCsvWriter(object):
    def __init__(self, path, tables):
        self._schema = tables
        self._files = {
            table: open(os.path.join(path, table + '.csv'), 'w', newline='')
            for table in tables.keys()
        }
        self._writers = {
            table: csv.DictWriter(self._files[table], [field[0] for field in fields])
            for table, fields in tables.items()
        }
        for writer in self._writers.values():
            writer.writeheader()

    def write(self, table, kv):
        values = {}
        closure = []
        for field_schema in self._schema[table]:
            name = field_schema[0]
            value_type = field_schema[1]

            closure.clear()
            closure.append(name)
            if len(field_schema) >= 3:
                closure.extend(field[2])

            for col in closure:
                value = kv.get(col)
                if value:
                    values[name] = value
                    break

        self._writers[table].writerow(values)



    def close(self):
        for f in self._files.values():
            f.close()
