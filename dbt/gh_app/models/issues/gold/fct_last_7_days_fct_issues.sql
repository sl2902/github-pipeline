

with 
    final as (
        select
            repo,
            created_at,
            last_7_days as issue_count
        from
            {{ ref('int_cumulative_issues') }}
        where
            created_at >= current_date - interval '7' day
    )
    select
        *
    from
        final