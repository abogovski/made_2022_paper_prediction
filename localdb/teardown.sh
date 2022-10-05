LOCALDB_DIR=$(dirname $0)/cluster
CLUSTER_NAME=made_papers_localdb
CLUSTER_VERSION=10

sudo pg_dropcluster --stop "$CLUSTER_VERSION" "$CLUSTER_NAME"
