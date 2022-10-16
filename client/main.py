import argparse
import json
import streamlit as st
import streamlit_authenticator as stauth
import psycopg
import os


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config')
    parser.add_argument('--default-paper-id', default=2)
    args = parser.parse_args()

    params = st.experimental_get_query_params()
    paper_id = int(params.get('paper_id', [args.default_paper_id])[0])
    st.experimental_set_query_params(paper_id=paper_id)

    with create_connection(get_config(args)) as connection:
        with connection.cursor() as cursor:
            render_paper(cursor, paper_id)
            connection.rollback()


if __name__ == '__main__':
    main()
