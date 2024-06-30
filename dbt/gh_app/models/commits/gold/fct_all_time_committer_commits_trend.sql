

with
    final as (
        select
            repo,
            commit_committer_date,
            num_commits
        from
            {{ ref('int_all_time_committer_commits_trend') }}
)
select
    *
from
    final