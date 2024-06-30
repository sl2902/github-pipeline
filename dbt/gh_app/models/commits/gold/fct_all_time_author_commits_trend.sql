
with
    final as (
        select
            repo,
            commit_author_date,
            num_commits
        from
            {{ ref('int_all_time_author_commits_trend') }}
)
select
    *
from
    final