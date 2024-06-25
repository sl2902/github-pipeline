
{{ config(
      materialized='incremental'
    , unique_key='stat_id'
    , incremental_strategy='merge'
    , on_schema_change='sync_all_columns'
    , properties={
      'format': "'PARQUET'"
    }
) }}


with 
    base as (
        select
            owner,
            repo,
            stat_id,
            fork_count,
            size_count,
            watchers_count,
            open_issues_count,
            network_count,
            stargazers_count,
            subscribers_count,
            created_at,
            pushed_at,
            updated_at,
            response,
            load_date,
            row_number() over(partition by stat_id order by updated_at desc) rank_dups
        from
            {{ source('bronze', 'base_repo') }}

        {% if is_incremental() %}
        where
            updated_at >= (SELECT max(updated_at) from {{ this }})

        {% endif %}
)
select
    owner,
    repo,
    stat_id,
    fork_count,
    size_count,
    watchers_count,
    open_issues_count,
    network_count,
    stargazers_count,
    subscribers_count,
    created_at,
    pushed_at,
    updated_at,
    response,
    load_date
from
    base
where
    rank_dups = 1