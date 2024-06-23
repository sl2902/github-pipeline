

with
    final as (
        select
            repo,
            created_at,
            num_issues
        from
            {{ ref('fct_all_time_issues_trend') }}
)
select
    *
from
    final