


with
    summary as (
        select
            repo,
            cast(commit_author_date as date) as commit_author_date,
            count(*) as num_commits
        from
            {{ ref('fct_commits') }}
        group by
            repo,
            cast(commit_author_date as date)
)
select
    *
from
    summary