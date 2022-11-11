import argparse
import streamlit as st
from utils import *


def render_paper(cursor, paper_id):
    paper = load_paper(cursor, paper_id)
    st.title(f'Paper {paper_id}')
    if paper['title'] is not None:
        st.header(paper['title'])

    if paper['year'] is not None:
        st.write('Year: ' + paper['year'])

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


def search_form(cursor):
    with st.form("my_form"):
        st.write("Choose paper parameters:")
        year_input = st.text_input(label='Year')
        abstract = st.checkbox('Abstract is not empty', value=True)
        title = st.checkbox('Title is not empty', value=True)

        submitted = st.form_submit_button("Submit")

    if submitted:
        num_rows = 5
        paper_ids = load_paper_ids(cursor, year_input, abstract, title, num_rows)
        search_len = len(paper_ids)
        num_rows = min(search_len, num_rows)
        paper_ids = paper_ids[:num_rows]

        if num_rows == 0:
            st.title(f'Nothing found')
            return
        st.title(f'Found {num_rows} papers')

        with st.container():
            for paper_id in paper_ids:
                paper = load_paper(cursor, paper_id)
                with st.expander(paper['title']):
                    render_paper(cursor, paper_id)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config')
    parser.add_argument('--default-paper-id', default=2)
    args = parser.parse_args()

    connection = create_connection(get_config(args))
    cursor = connection.cursor()

    params = st.experimental_get_query_params()
    paper_id = int(params.get('paper_id', [args.default_paper_id])[0])
    st.experimental_set_query_params(paper_id=paper_id)

    st.title("Team 14")
    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            hashed_pswd = make_hashes(password)

            result = login_user(cursor, username, check_hashes(password, hashed_pswd))
            if result:
                st.success("Logged In as {}".format(username))
                search_form(cursor)
                connection.rollback()
            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            add_userdata(connection, cursor, new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")


if __name__ == '__main__':
    main()
