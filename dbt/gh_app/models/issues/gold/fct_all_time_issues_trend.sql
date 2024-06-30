

with
    final as (
        select
            repo,
            created_at,
            num_issues
        from
            {{ ref('int_all_time_issues_trend') }}
)
select
    *
from
    final