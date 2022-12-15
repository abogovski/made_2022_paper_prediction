CONN_STR="host=localhost port=6432 dbname=paper_prediction user=team_14"
export PGPASSWORD=local_team14_password

psql "$CONN_STR" -f tools/analytics_builder/top_n_authors.sql