import hashlib
import os
import psycopg
import json


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


def create_usertable(cursor):
    cursor.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(connection, cursor, username, password):
    cursor.execute('INSERT INTO userstable(username,password) VALUES (%s, %s)', (username, password))
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
    columns = ('paper_id', 'doi', 'title', 'abstract')
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


def load_authors(cursor, paper_id):
    columns = ('author_id', 'name', 'position', 'email')
    assert type(paper_id) == int
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

    with open(args.config) as f:
        return json.load(f)


def create_connection(cfg):
    conn_str = ' '.join(f'{key}={value}' for key, value in cfg.items())
    return psycopg.connect(conn_str)
