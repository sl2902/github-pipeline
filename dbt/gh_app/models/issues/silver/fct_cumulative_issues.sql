with
    summary as (
        select 
	        repo
            ,cast(created_at as date) as created_at
            ,count(*) over(partition by repo order by cast(created_at as date)
            range between interval '6' day preceding and current row) as last_7_days
        from 
            {{ ref('fct_issues') }}
        group by
            repo
            ,cast(created_at as date)
)
select
    *
from
    summary