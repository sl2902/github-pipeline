


with
    summary as (
        select
            repo,
            date_diff('day', created_at, updated_at) as num_days,
            extract(month from cast(created_at as date)) month,
            count(*) num_issues
        from
            {{ ref('stg_issues') }}
        where 
            extract(month from cast(created_at as date)) = extract(month from current_date) - 1
        and
            extract(year from cast(created_at as date)) = extract(year from current_date)
        group by
            repo,
            date_diff('day', created_at, updated_at),
            extract(month from cast(created_at as date))
        order by 
            num_days
)
select
    *
from
    summary