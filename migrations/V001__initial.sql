CREATE SCHEMA IF NOT EXISTS dataset;

/************/
/* Entities */
/************/

CREATE TABLE IF NOT EXISTS dataset.paper (
    paper_id bigserial PRIMARY KEY,
    _id text,

    title text,
    abstract text,
    lang text,
    pdf text,

    doi text,
    isbn text,
    issn text,
    issue text,
    volume text,
    year text,
    page_start text,
    page_end text,

    n_citation bigint /* NOT NULL ? */
);

CREATE TABLE IF NOT EXISTS dataset.author (
    author_id bigserial PRIMARY KEY,
    _id text,

    avatar text,
    bio text,
    email text,
    position text,
    /* homepage text, -- only three occurences in the entire dataset */
    name text,
    orcid text

    /*oid text,*/
    /*gid text,*/

    /* name_zh text, -- 2603 occurences */
    /* oid_zh text, -- 233 occurences */
    /* org_zh text, -- 4k occurences */
    /* orgid bytea, -- not sure what to do with this id */
);

CREATE TABLE IF NOT EXISTS dataset.org (
    org_id bigserial PRIMARY KEY,
    name text
);

CREATE TABLE IF NOT EXISTS dataset.venue (
    venue_id bigserial PRIMARY KEY,
    _id text,

    issn text,
    online_issn text,
    publisher text, 
    sid text,
    name text,
    raw text,
    t text,
    type text
);

CREATE TABLE IF NOT EXISTS dataset.fos (
    fos_id bigserial PRIMARY KEY,
    value text NOT NULL
);

CREATE TABLE IF NOT EXISTS dataset.keyword (
    keyword_id bigserial PRIMARY KEY,
    value text NOT NULL
);

/*************/
/* Relations */
/*************/

CREATE TABLE IF NOT EXISTS dataset.paper_author (
    paper_id bigint NOT NULL,
    author_id bigint NOT NULL,

    PRIMARY KEY (paper_id, author_id)
);

CREATE TABLE IF NOT EXISTS dataset.author_org (
    author_id bigint NOT NULL,
    org_id bigint NOT NULL,

    PRIMARY KEY (author_id, org_id)
);

/* There could be a case for paper_org relation. Let's drop it, for now */

CREATE TABLE IF NOT EXISTS dataset.paper_venue (
    paper_id bigint PRIMARY KEY,
    venue_id bigint NOT NULL
);

CREATE TABLE IF NOT EXISTS dataset.paper_fos (
    paper_id bigint NOT NULL,
    fos_id bigint NOT NULL,

    PRIMARY KEY (paper_id, fos_id)
);

CREATE TABLE IF NOT EXISTS dataset.paper_keyword (
    paper_id bigint NOT NULL,
    keyword_id bigint NOT NULL,

    PRIMARY KEY (paper_id, keyword_id)
);

CREATE TABLE IF NOT EXISTS dataset.paper_reference (
    referrer_paper_id bigint NOT NULL,
    reference_paper_id bigint NOT NULL,

    PRIMARY KEY (referrer_paper_id, reference_paper_id)
);

CREATE TABLE IF NOT EXISTS dataset.paper_url (
    paper_id bigint NOT NULL,
    url text NOT NULL,

    PRIMARY KEY (paper_id, url)
);
