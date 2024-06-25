{{ config(
      materialized='incremental'
    , unique_key='id'
    , incremental_strategy='merge'
    , on_schema_change='sync_all_columns'
    , properties={
      'format': "'PARQUET'"
    }
) }}

with
    staging as (
        select
            id
            ,response
            ,created_at
            ,row_number() over(partition by id order by created_at desc) as rank_dups
        from
            {{ source('bronze', 'issues') }}
            {% if is_incremental() %}
        where
            created_at >= (SELECT max(created_at) from {{ this }})

        {% endif %}
)
select
    id
    ,response
    ,created_at
from
    staging
where
    rank_dups = 1
