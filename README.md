# MADE 2022: Paper prediction project

## Local database management

```bash
./localdb/setup.sh # create local standalone cluster with blank paper_prediction database
./localdb/teardown.sh # teardown local standalone cluster
```

## Setting up database schema
```bash
python tools/client/apply_sql.py migrations/V001__initial.sql cfg/localdb.json
```

## Uploading dataset
```bash
mkdir data/csv_tables
python tools/dataset_parsing/collect_csv_tables.py data/dblpv13.json data/csv_tables/
python tools/client/bulk_upload.py data/csv_tables/ cfg/localdb.json
```

## Setting update local streamlit

```
streamlit run client/main.py cfg/remote-db-readaccess.json
```
