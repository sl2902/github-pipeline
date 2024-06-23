

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
            created_date
        from
            {{ source('bronze', 'commits') }}
)
select
    *
from
    base
