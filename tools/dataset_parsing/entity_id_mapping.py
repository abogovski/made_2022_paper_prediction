import os
import csv


class IdMapping(object):
    def __init__(self, path, entity, ident):
        self._path = path
        self._entity = entity
        self._ident = ident

        self._values = []
        self._value_to_id = {}

    def __getitem__(self, value):
        value_id = self._value_to_id.get(value)
        exists = value_id is not None

        if not exists:
            self._values.append(value)
            value_id = len(self._values)
            self._value_to_id[value] = value_id

        return value_id, not exists

    def close(self):
        with open(os.path.join(self._path, self._entity + '_ids.csv'), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([self._entity + '_id', self._ident])
            for i, value in enumerate(self._values):
                writer.writerow([i + 1, value])


class EntityIdMapping(object):
    def __init__(self, path, entity_idents):
        self._id_mappings = {
            entity: IdMapping(path, entity, ident)
            for entity, ident in entity_idents.items()
        }

    def __getitem__(self, entity):
        return self._id_mappings[entity]

    def close(self):
        for id_mapping in self._id_mappings.values():
            id_mapping.close()
