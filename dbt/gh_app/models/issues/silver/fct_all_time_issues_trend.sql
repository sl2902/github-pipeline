

with
    summary as (
        select
            repo,
            cast(created_at as date) as created_at,
            count(*) as num_issues
        from
            {{ ref('fct_issues') }}
        group by
            repo,
            cast(created_at as date)
)
select
    *
from
    summary