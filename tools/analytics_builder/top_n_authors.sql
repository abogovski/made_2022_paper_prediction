CREATE TABLE  IF NOT EXISTS dataset.paper_with_tag AS
  SELECT p.paper_id,
         p.n_citation,
         t.tag
  FROM   dataset.paper p
         JOIN dataset.paper_tags t
           ON p._id = t._id;

CREATE TABLE  IF NOT EXISTS dataset.paper_with_tag_author AS
  SELECT p.*,
         a.*
  FROM   dataset.paper_with_tag p
         JOIN dataset.paper_author pa
           ON p.paper_id = pa.paper_id
         JOIN dataset.author a
           ON a.author_id = pa.author_id;

CREATE TABLE  IF NOT EXISTS dataset.top_10_author AS
  SELECT *
  FROM   (SELECT *,
                 Rank()
                   OVER (
                     partition BY tag
                     ORDER BY n_citation DESC)
          FROM   dataset.paper_with_tag_author
          WHERE  n_citation IS NOT NULL) AS foo
  WHERE  rank <= 10;


CREATE TABLE  IF NOT EXISTS dataset.tags AS
SELECT distinct tag FROM dataset.paper_with_tag_author;

DROP TABLE dataset.paper_with_tag_author;
DROP TABLE dataset.paper_with_tag;