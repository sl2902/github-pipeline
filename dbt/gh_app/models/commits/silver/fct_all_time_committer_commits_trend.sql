

with
    summary as (
        select
            repo,
            cast(commit_committer_date as date) as committer_commit_date,
            count(*) as num_commits
        from
            {{ ref('fct_commits') }}
        group by
            repo,
            cast(commit_committer_date as date)
)
select
    *
from
    summary