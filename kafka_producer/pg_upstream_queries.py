raw_qry_str = {
    "commits":  """
                select 
                    owner
                    ,repo
                    ,response->>'sha' as commit_sha
                    ,response ->>'url' as url
                    ,(response ->'commit'->>'comment_count')::int as comment_count
                    ,response->'commit'->>'message' as commit_message
                    ,(response->'author'->>'id')::bigint as author_id
                    ,response->'author'->>'login' as author_login
                    ,response->'author'->>'type' as author_type
                    ,response->'commit'->'author'->>'name' as author_name
                    ,(response->'commit'->'author'->>'date')::timestamp as commit_author_date
                    ,response->'commit'->'author'->>'email' as commit_author_email
                    ,(response->'committer'->>'id')::bigint as committer_id
                    ,response->'committer'->>'login' as committer_login 
                    ,response->'committer'->>'type' as committer_type
                    ,response->'commit'->'committer'->>'name' as committer_name
                    ,(response->'commit'->'committer'->>'date')::timestamp as commit_committer_date
                    ,response->'commit'->'committer'->>'email' as commit_committer_email
                    ,response->'commit'->'verification'->>'reason' as commit_verification_reason
                    ,(response->'commit'->'verification'->>'verified')::boolean as commit_verification_verified
                    ,response::text
                    ,created_date as load_date
                
                from 
                    gh_staging_raw_endpoints
                where 
                    endpoint = 'commits';
                """,
    "issues":   """
                select
                    owner
                    ,repo
                    ,(response ->>'id')::bigint AS id
                    ,(response ->>'number')::bigint AS number
                    ,response ->>'title' AS title
                    ,response ->>'state' AS state
                    ,(response ->>'created_at')::timestamp AS created_at
                    ,(response ->>'updated_at')::timestamp AS updated_at
                    ,(response ->>'closed_at')::timestamp AS closed_at
                    ,(response ->>'comments')::bigint AS comments
                    ,(response ->>'draft')::boolean AS draft
                    ,response ->>'author_association' AS author_association
                    ,(response ->'user'->>'id')::bigint AS user_id
                    ,(response ->'labels'->0->>'id')::bigint AS label_id
                    ,response ->>'repository_url' AS repository_url
                    ,(response ->'reactions'->>'total_count')::int AS total_count
                    ,(response ->'reactions'->>'+1')::int AS plus1
                    ,(response ->'reactions'->>'-1')::int AS minus1
                    ,(response ->'reactions'->>'laugh')::int AS laugh
                    ,(response ->'reactions'->>'hooray')::int AS hooray
                    ,(response ->'reactions'->>'confused')::int AS confused
                    ,(response ->'reactions'->>'heart')::int AS heart
                    ,(response ->'reactions'->>'rocket')::int AS rocket
                    ,(response ->'reactions'->>'eyes')::int AS eyes
                    ,response::text
                    ,created_date as load_date
                FROM 
                    gh_staging_raw_endpoints
                where 
                    endpoint = 'issues'

                """,
    "/":        """
                select 
                    response ->'id' as stat_id
                    ,owner
                    ,response ->>'name' as repo
                    ,(response ->>'forks')::int as fork_count
                    ,(response ->>'size')::int as size_count
                    ,(response ->>'watchers')::int as watchers_count
                    ,(response ->>'open_issues')::int as open_issues_count
                    ,(response ->>'network_count')::int as network_count
                    ,(response ->>'stargazers_count')::int as stargazers_count
                    ,(response ->>'subscribers_count')::int as subscribers_count
                    ,(response ->>'created_at')::timestamp as created_at
                    ,(response ->>'pushed_at')::timestamp as pushed_at
                    ,(response ->>'updated_at')::timestamp as updated_at
                    ,response::text
                    ,created_date as load_date
                from
                    gh_staging_raw_endpoints
                where 
                    endpoint = '/'

                """ 
}
