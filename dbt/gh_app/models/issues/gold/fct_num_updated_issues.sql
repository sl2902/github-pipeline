

with
    final as (
        select
            repo,
            num_days,
            num_issues
        from
            {{ ref('int_count_updated_issues') }}
)
select
    *
from
    final