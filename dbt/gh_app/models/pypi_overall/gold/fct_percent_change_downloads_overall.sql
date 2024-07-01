with
    final as (
        select
            id,
            package,
            category,
            date,
            downloads,
            percent_change,
            load_date
        from
            {{ ref('int_percent_change_downloads_overall') }}
)
select
    *
from
    final