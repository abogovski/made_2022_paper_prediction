# MADE 2022: Paper prediction project

## Local database management

```bash
./localdb/reset.sh # reset localdb & setup schema
./localdb/teardown.sh # teardown localdb
```

## Setting up database schema manually
```bash
python tools/client/apply_sql.py migrations/V001__initial.sql cfg/localdb.json
```

## Uploading dataset
```bash
wget https://originalstatic.aminer.cn/misc/dblp.v13.7z -O data/dblpv13.7z
7z x data/dblpv13.7z -odata/

mkdir data/csv_tables
python tools/dataset_parsing/collect_csv_tables.py data/dblpv13.json data/csv_tables/
python tools/client/bulk_upload.py data/csv_tables/ cfg/localdb.json
```

## Setting update local streamlit

```
streamlit run client/main.py cfg/remote-db-readaccess.json
```
