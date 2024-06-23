

with    
    final as (
        select
            repo,
            committer_name,
            num_commits
        from
            {{ ref('fct_num_committer_commits') }}
)
select
    *
from
    final