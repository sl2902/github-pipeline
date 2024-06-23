

with
    final as (
        select
            repo,
            committer_commit_date,
            num_commits
        from
            {{ ref('fct_all_time_committer_commits_trend') }}
)
select
    *
from
    final