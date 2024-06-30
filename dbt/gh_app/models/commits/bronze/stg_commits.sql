{{ config(
      materialized='incremental'
    , unique_key='commit_sha'
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
            commit_sha,
            url,
            comment_count,
            commit_message,
            author_id,
            author_login,
            author_type,
            author_name,
            commit_author_date,
            commit_author_email,
            committer_id,
            committer_login,
            committer_type,
            committer_name,
            commit_committer_date,
            commit_committer_email,
            commit_verification_reason,
            commit_verification_verified,
            response,
            load_date,
            row_number() over(partition by commit_sha order by commit_author_date desc) as rank_dups
        from
            {{ source('trino', 'commits') }}

            {% if is_incremental() %}
        where
            commit_author_date >= (SELECT max(commit_author_date) from {{ this }})

        {% endif %}
)
select
    owner,
    repo,
    commit_sha,
    url,
    comment_count,
    commit_message,
    author_id,
    author_login,
    author_type,
    author_name,
    commit_author_date,
    commit_author_email,
    committer_id,
    committer_login,
    committer_type,
    committer_name,
    commit_committer_date,
    commit_committer_email,
    commit_verification_reason,
    commit_verification_verified,
    response,
    load_date
from
    base
where
    rank_dups = 1
