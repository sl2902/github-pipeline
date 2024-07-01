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
            ,package
            ,endpoint
            ,category
            ,date
            ,downloads
            ,load_date
            ,row_number() over(partition by id order by load_date desc) as rank_dups
        from
            {{ source('trino', 'overall') }}
        
        {% if is_incremental() %}
        where
            load_date > (SELECT max(load_date) from {{ this }})

        {% endif %}
)
select
       id
        ,package
        ,endpoint
        ,category
        ,date
        ,downloads
        ,load_date
from
    staging
where
    rank_dups = 1