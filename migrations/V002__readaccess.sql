CREATE ROLE paper_prediction_readaccess;
GRANT CONNECT ON DATABASE paper_prediction TO paper_prediction_readaccess;
GRANT USAGE ON SCHEMA dataset TO paper_prediction_readaccess;
GRANT SELECT ON ALL TABLES IN SCHEMA dataset TO paper_prediction_readaccess;

CREATE USER made_guest WITH PASSWORD 'made_guest';
GRANT paper_prediction_readaccess TO made_guest;
