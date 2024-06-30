

with
  	rank_committer as (
		  select 
		    repo,
		    committer_name,
		    count(*) num_commits,
		    dense_rank() over(partition by repo order by count(*) desc) rr_committer
		  from
		     {{ ref('stg_commits') }}
		   group by
		      repo,
		      committer_name
)
select
    repo,
    committer_name,
    num_commits
from
    rank_committer
where 
    rr_committer < 4
order by 
    repo,
    num_commits desc