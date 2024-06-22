{{ 
    config(materialized='table') 
}}

with
    staging as (
        select
            id
            ,response
        from
            {{ source('bronze', 'issues') }}
)
select
    *
from
    staging
