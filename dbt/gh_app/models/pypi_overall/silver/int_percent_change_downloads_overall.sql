with
    int as (
        select
            id,
            package,
            category,
            date,
            downloads,
            lag(downloads, 1) over(partition by package, category order by date) as prev_download,
            (1 - 1. * lag(downloads, 1) over(partition by package, category order by date)/cast(downloads as double)) as percent_change,
            load_date
        from
            {{ ref('stg_overall') }}
)
select
    *
from
    int
