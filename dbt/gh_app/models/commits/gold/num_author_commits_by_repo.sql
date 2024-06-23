

with    
    final as (
        select
            repo,
            author_name,
            num_commits
        from
            {{ ref('fct_num_author_commits') }}
)
select
    *
from
    final