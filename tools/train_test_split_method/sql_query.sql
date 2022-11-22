with keyword_links as
(select
    array_agg(paper_id) as links,
    keyword_id
from paper_keyword t1
group by keyword_id)

select *
from keyword_links
where 1 < array_length(links, 1)
  and array_length(links, 1) < 6;
