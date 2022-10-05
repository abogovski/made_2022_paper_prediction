LOCALDB_DIR=$(realpath $(dirname $0)/cluster)
PORT=5433
DBNAME="paper_prediction"
PGUSR=team_14
export PGPASSWORD=local_team14_password

CLUSTER_NAME=made_papers_localdb
CLUSTER_VERSION=10

mkdir "$LOCALDB_DIR"
sudo chown postgres "$LOCALDB_DIR"
sudo -u postgres pg_createcluster "$CLUSTER_VERSION" "$CLUSTER_NAME" -D "$LOCALDB_DIR"

sudo -u postgres pg_ctlcluster "$CLUSTER_VERSION" "$CLUSTER_NAME" start -o "-F -p $PORT"
sudo -u postgres psql --port $PORT -c "CREATE USER $PGUSR WITH PASSWORD '$PGPASSWORD' CREATEDB"
psql --host localhost --port $PORT --dbname postgres --user $PGUSR -c "CREATE DATABASE $DBNAME WITH ENCODING 'UTF-8'"
