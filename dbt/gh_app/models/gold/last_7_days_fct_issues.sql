

with 
    final as (
        select
            repo,
            created_at,
            last_7_days as issue_count
        from
            {{ ref('fct_cumulative_issues') }}
    )
    select
        *
    from
        final