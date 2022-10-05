import argparse
from contextlib import closing

from dataset import read_dataset
from entity_id_mapping import EntityIdMapping
from multi_csv_writer import MultiCsvWriter
from csv_schema import CSV_SCHEMA


ENTITY_IDENTS = {
    'paper':   '_id',
    'author':  '_id',
    'venue':   '_id',
    'org':     'name',
    'fos':     'value',
    'keyword': 'value',
}

def replace_null_chars(s):
    if s is None:
        return None
    return s.replace('\x00', ' ')


def normalize(s):
    return None if s is None else ' '.join(s.lower().split())


def coalesce(kv, *keys):
    for key in keys:
        value = kv.get(key)
        if value is not None:
            break
    return value


def ensure_value_or_make_unknown(entry, field, src_fields):
    value = normalize(coalesce(entry, *src_fields))
    if not value:
        entry.clear()
        value = 'unknown'
    entry[field] = value


def write_if_firstmet(writer, entity_id_mapping, entry, entity, ident_field):
    entry[entity + '_id'], id_created = entity_id_mapping[entity][entry[ident_field]]
    if id_created:
        writer.write(entity, entry)
    return id_created


def collect_orgs(author):
    orgs = []
    if author.get('org'):
        orgs.append(author['org'])
    elif author.get('org_zh'):
        orgs.append(author['org_zh'])

    if author.get('orgs'):
        orgs.extend(author['orgs'])
    elif author.get('orgs_zh'):
        orgs.extend(author['orgs_zh'])

    return set(filter(bool, orgs))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_path')
    parser.add_argument('csv_tables_path')
    args = parser.parse_args()

    with closing(MultiCsvWriter(args.csv_tables_path, CSV_SCHEMA)) as writer:
        with closing(EntityIdMapping(args.csv_tables_path, ENTITY_IDENTS)) as entity_id_mapping:
            for paper in read_dataset(args.dataset_path):
                paper['paper_id'], _ = entity_id_mapping['paper'][paper['_id']]
                paper['abstract'] = replace_null_chars(paper.get('abstract')) # NOTE: null characters cause problems on upload to postgres
                writer.write('paper', paper)

                for author in paper.get('authors', []):
                    author_created = ensure_value_or_make_unknown(author, 'name', ['name', 'name_zh'])
                    if author_created:  # WRN: possible loss of orgs
                        write_if_firstmet(writer, entity_id_mapping, author, 'author', 'name')
                        writer.write('paper_author', {'paper_id': paper['paper_id'], 'author_id': author['author_id']})
                        for org in scollect_orgs(author):
                            ensure_value_or_make_unknown(org, 'name', ['name'])
                            write_if_firstmet(writer, entity_id_mapping, org, 'org', 'name')
                            writer.write('paper_org', {'paper_id': paper['paper_id'], 'org_id': org['org_id']})

                venue = paper.get('venue')
                if venue:
                    ensure_value_or_make_unknown(venue, 'name', ['name_d', 'raw', 'name_s', 'sid', 'name_zh', 'raw_zh'])
                    write_if_firstmet(writer, entity_id_mapping, venue, 'venue', 'name')

                reference_paper_ids = set(entity_id_mapping['paper'][ref][0] for ref in paper.get('references', []))
                for reference_paper_id in reference_paper_ids:
                    # WRN: hanging reference_paper_id values are possible in paper_reference table
                    writer.write('paper_reference', {'referrer_paper_id': paper['paper_id'], 'reference_paper_id': reference_paper_id})

                for field, entity in [('fos', 'fos'), ('keywords', 'keyword')]:
                    for value in set(map(normalize, paper.get(field, []))):
                        if value:
                            entry = {'value': value}
                            write_if_firstmet(writer, entity_id_mapping, entry, entity, 'value')
                            writer.write('paper_' + entity, {'paper_id': paper['paper_id'], entity + '_id': entry[entity + '_id']})

                for url in set(map(str.strip, paper.get('urls', []))):
                    writer.write('paper_url', {'paper_id': paper['paper_id'], 'url': url})


if __name__ == '__main__':
    main()
