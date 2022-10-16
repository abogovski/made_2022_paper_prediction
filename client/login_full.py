import streamlit as st
import pandas as pd
import psycopg
import json
import hashlib
import argparse
import os


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


def create_connection(cfg):
    conn_str = ' '.join(f'{key}={value}' for key, value in cfg.items())
    return psycopg.connect(conn_str)





# DB  Functions
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


def render_paper(cursor, paper_id):
    paper = load_paper(cursor, paper_id)
    st.title(f'Paper {paper_id}')
    if paper['title'] is not None:
        st.header(paper['title'])

    if paper['doi'] is not None:
        st.write('DOI: ' + paper['doi'])

    authors = []
    for author in load_authors(cursor, paper_id):
        author_str = (author['name'] or '') + ' ' + (author['position'] or '')
        author_str = author_str.strip() or 'unknown'
        if author['email'] is not None:
            author_str += ' (' + author['email'] + ')'
        authors.append(author_str)
    st.markdown('_' + ', '.join(authors) + '_')

    if paper['abstract'] is not None:
        st.subheader('Abstract')
        st.write(paper['abstract'])


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


def main():
    """Simple Login App"""
    # DB Management
    # config_path = "localdb.json"
    # with open(config_path) as file:
    #     cfg = json.load(file)
    # connection = create_connection(cfg)
    # cursor = connection.cursor()

    parser = argparse.ArgumentParser()
    parser.add_argument('--config')
    parser.add_argument('--default-paper-id', default=2)
    args = parser.parse_args()

    connection = create_connection(get_config(args))
    cursor = connection.cursor()

    # with create_connection(get_config(args)) as connection:
    #     with connection.cursor() as cursor:

    params = st.experimental_get_query_params()
    paper_id = int(params.get('paper_id', [args.default_paper_id])[0])
    st.experimental_set_query_params(paper_id=paper_id)

    st.title("Team 14")
    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            # if password == '12345':
            create_usertable(cursor)
            hashed_pswd = make_hashes(password)

            result = login_user(cursor, username, check_hashes(password, hashed_pswd))
            if result:

                st.success("Logged In as {}".format(username))

                paper_id = 2
                st.experimental_set_query_params(paper_id=paper_id)

                render_paper(cursor, paper_id)
                connection.rollback()

            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable(cursor)
            add_userdata(connection, cursor, new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")


if __name__ == '__main__':
    main()
