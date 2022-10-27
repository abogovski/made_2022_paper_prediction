import streamlit as st
import argparse
from utils import *


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
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
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
