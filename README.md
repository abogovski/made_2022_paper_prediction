# MADE 2022: Paper prediction project

## Development

### Setting up local database

Reset `paper_prediction_localdb` container and apply migrations:

```bash
./tools/localdb/reset.sh
```

On ubuntu database should accessable via
```bash
PGPASSWORD=local_team14_password psql "host=localhost port=6432 dbname=paper_prediction user=team_14"
```
and
```bash
python -m tools.dbclient apply_sql file.sql cfg/localdb.json
```

### Development container

Reset/created development container using local repository snapshot
```base
./tools/development_container/reset.sh
```

Directory `./data` is mounted as writeable docker volume.
```
./tools/development_container/exec.sh touch /paper_prediction/data/newfile.txt
ls data/newfile.txt
```

Local database is available over docker network
```
./tools/development_container/exec.sh \
  python -m tools.dbclient apply_sql container-file.sql cfg/localdb-development.json
```

## Uploading dataset
```bash
wget https://originalstatic.aminer.cn/misc/dblp.v13.7z -O data/dblpv13.7z
7z x data/dblpv13.7z -odata/
```

Download archive with tags
`https://drive.google.com/file/d/1H5FqXsP2qPuXwjFw6M9qJr784ivWOS2r/view?usp=share_link`
extract `.csv` data and move to `/data/csv_tables/paper_tags.csv`

```
python -m tools.dataset_parsing collect_csv_tables data/dblpv13.json data/csv_tables/
python -m tools.dbclient bulk_upload data/csv_tables/ cfg/localdb.json
```

## Uploading tags info
```bash
./tools/analytics_builder/exec.sh 
```

## Setting up local streamlit

```
streamlit run client/main.py -- --config cfg/localdb.json 
```

## Database schema
![alt text](db-schema.svg?raw=true)
