

with
    final as (
        select
            repo,
            num_days,
            num_issues
        from
            {{ ref('fct_count_updated_issues') }}
)
select
    *
from
    final