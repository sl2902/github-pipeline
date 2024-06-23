
with
    final as (
        select
            repo,
            commit_author_date,
            num_commits
        from
            {{ ref('fct_all_time_author_commits_trend') }}
)
select
    *
from
    final