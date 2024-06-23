{{ 
    config(materialized='table') 
}}

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
        from
            {{ source('bronze', 'issues') }}
)
select
    *
from
    staging
