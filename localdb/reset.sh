cd $(dirname $0)
docker-compose down
docker-compose build --no-cache
docker-compose up --detach --force-recreate

CONN_STR="host=localhost port=6432 dbname=paper_prediction user=team_14"
export PGPASSWORD=local_team14_password

echo -n "Awaiting successful SELECT TRUE "
until psql "$CONN_STR" -c "SELECT TRUE" >/dev/null 2>&1; do
    echo -n .
    sleep 0.5
done
echo

for FNAME in $(find ../migrations -name "V*__*.sql" | sort); do
    echo "Applying $(basename $FNAME) migration"
    psql "$CONN_STR" -f $FNAME
done
