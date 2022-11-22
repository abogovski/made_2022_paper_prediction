Train-test-split method
---
### Algorithm description
Algorithm is described in [report.md](https://github.com/abogovski/made_2022_paper_prediction/blob/train_test_split/tools/train_test_split_method/report.md)

### Final result
Ids of papers are stored in `outputs/test_paper_id_csv` and 
`outputs/train_paper_id_csv` respectively.

### Reproduce results:

Run
```
pip install -r requirements.txt
```
Change database credentials in `db_config.txt`.
Default value is 
```
host=localhost port=6432 dbname=paper_prediction user=team_14 password=local_team14_password
``` 
Run
```
python train_test_split.py
```
