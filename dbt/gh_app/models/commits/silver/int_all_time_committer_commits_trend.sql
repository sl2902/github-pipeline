

with
    summary as (
        select
            repo,
            cast(commit_committer_date as date) as commit_committer_date,
            count(*) as num_commits
        from
            {{ ref('stg_commits') }}
        group by
            repo,
            cast(commit_committer_date as date)
)
select
    *
from
    summary