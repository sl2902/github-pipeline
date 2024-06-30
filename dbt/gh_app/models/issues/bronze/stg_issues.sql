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
            ,owner
            ,repo
            ,number
            ,title
            ,state
            ,created_at
            ,updated_at
            ,closed_at
            ,comments
            ,draft
            ,author_association
            ,user_id
            ,label_id
            ,repository_url
            ,total_count
            ,plus1
            ,minus1
            ,laugh
            ,hooray
            ,confused
            ,heart
            ,rocket
            ,eyes
            ,response
            ,load_date
            ,row_number() over(partition by id order by load_date desc) as rank_dups
        from
            {{ source('trino', 'issues') }}
        
            {% if is_incremental() %}
        where
            load_date > (SELECT max(load_date) from {{ this }})

        {% endif %}
)
select
        id
        ,owner
        ,repo
        ,number
        ,title
        ,state
        ,created_at
        ,updated_at
        ,closed_at
        ,comments
        ,draft
        ,author_association
        ,user_id
        ,label_id
        ,repository_url
        ,total_count
        ,plus1
        ,minus1
        ,laugh
        ,hooray
        ,confused
        ,heart
        ,rocket
        ,eyes
        ,response
        ,load_date
from
    staging
where
    rank_dups = 1
