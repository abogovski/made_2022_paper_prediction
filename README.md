# MADE 2022: Paper prediction project

## Local database management

```bash
./tools/localdb/reset.sh # reset localdb & setup schema
./tools/localdb/teardown.sh # teardown localdb
```

## Setting up database schema manually
```bash
python -m tools.dbclient apply_sql cfg/localdb.json migrations/V001__initial.sql
```

## Uploading dataset
```bash
wget https://originalstatic.aminer.cn/misc/dblp.v13.7z -O data/dblpv13.7z
7z x data/dblpv13.7z -odata/

python -m tools.dataset_parsing collect_csv_tables data/dblpv13.json data/csv_tables/
python -m tools.dbclient bulk_upload data/csv_tables/ cfg/localdb.json
```

## Setting update local streamlit

```
streamlit run client/main.py cfg/remotedb-readaccess.json
```
