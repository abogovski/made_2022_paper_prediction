import hashlib
import os
import json
import psycopg


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


def add_userdata(connection, cursor, username, password):
    cursor.execute('INSERT INTO userstable(user_id, username,password) VALUES (nextval("users_seq"), %s, %s)',
                   (username, password))
    connection.commit()


def login_user(cursor, username, password):
    cursor.execute('SELECT * FROM userstable WHERE username =%s AND password = %s', (username, password))
    data = cursor.fetchall()
    return data


def view_all_users(cursor):
    cursor.execute('SELECT * FROM userstable')
    data = cursor.fetchall()
    return data


def load_paper(cursor, paper_id):
    columns = ('paper_id', 'doi', 'title', 'abstract', 'year')
    cursor.execute(
        f'''
        SELECT {', '.join(columns)}
        FROM dataset.paper
        WHERE paper_id = {paper_id}
        '''
    )
    papers = cursor.fetchall()
    if len(papers) != 1:
        raise RuntimeError(f'{len(papers)} papers found by id={paper_id}')
    return dict(zip(columns, papers[0]))


def load_paper_ids(cursor, year, abstract, title, limit_rows=10):
    abstract_data = 'not NULL' if abstract else 'NULL'
    title_data = 'not NULL' if title else 'NULL'

    cursor.execute(
        f'''
        SELECT paper_id
        FROM dataset.paper
        WHERE year = %s
        and abstract is {abstract_data}
        and title  is {title_data}
        limit %s
        ''',
        (str(year), limit_rows)
    )
    papers = cursor.fetchall()
    print(papers)
    data = [paper_id[0] for paper_id in papers]
    return data


def load_authors(cursor, paper_id):
    columns = ('author_id', 'name', 'position', 'email')
    assert isinstance(paper_id, int)
    cursor.execute(
        f'''
        SELECT {', '.join(columns)}
        FROM dataset.paper_author JOIN dataset.author USING (author_id)
        WHERE paper_id = {paper_id}
        '''
    )

    authors = []
    for values in cursor.fetchall():
        authors.append(dict(zip(columns, values)))
    return authors


def get_config(args):
    if args.config is None:
        return {
            'host':     os.environ['PAPER_DB_HOST'],
            'port':     os.environ['PAPER_DB_PORT'],
            'dbname':   os.environ['PAPER_DB_NAME'],
            'user':     os.environ['PAPER_DB_USER'],
            'password': os.environ['PAPER_DB_PASSWORD']
        }

    with open(args.config) as file:
        return json.load(file)


def create_connection(cfg):
    conn_str = ' '.join(f'{key}={value}' for key, value in cfg.items())
    return psycopg.connect(conn_str)
