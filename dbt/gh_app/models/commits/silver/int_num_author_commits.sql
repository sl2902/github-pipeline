

with
  	rank_author as (
		  select 
		    repo,
		    author_name,
		    count(*) num_commits,
		    dense_rank() over(partition by repo order by count(*) desc) rr_author
		  from
		     {{ ref('stg_commits') }}
		   group by
		      repo,
		      author_name
		    order by 
		    repo,
		    num_commits desc
)
select
    repo,
    author_name,
    num_commits
from
    rank_author
where 
    rr_author < 4