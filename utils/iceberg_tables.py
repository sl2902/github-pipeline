ice_tables = {
    "commits": """
                create table if not exists bronze.commits (
                    owner STRING,
                    repo STRING,
                    commit_sha STRING,
                    url STRING,
                    comment_count INT,
                    commit_message STRING,
                    author_id LONG,
                    author_login STRING,
                    author_type STRING,
                    author_name STRING,
                    commit_author_date TIMESTAMP,
                    commit_author_email STRING,
                    committer_id LONG,
                    committer_login STRING,
                    committer_type STRING,
                    committer_name STRING,
                    commit_committer_date TIMESTAMP,
                    commit_committer_email STRING,
                    commit_verification_reason STRING,
                    commit_verification_verified BOOLEAN,
                    response STRING,
                    load_date TIMESTAMP
               )
               using iceberg
               location '{}'
               partitioned by (days(load_date));
                """,
    "issues": """
                create table if not exists bronze.issues (
                    owner STRING,
                    repo STRING,
                    id BIGINT,
                    number BIGINT,
                    title STRING,
                    state STRING,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP,
                    closed_at TIMESTAMP,
                    comments BIGINT,
                    draft BOOLEAN,
                    author_association STRING,
                    user_id BIGINT,
                    label_id BIGINT,
                    repository_url STRING,
                    total_count INT,
                    plus1 INT,
                    minus1 INT,
                    laugh INT,
                    hooray INT,
                    confused INT,
                    heart INT,
                    rocket INT,
                    eyes INT,
                    response STRING,
                    load_date TIMESTAMP
                )
                using iceberg
                location '{}'
                partitioned by (days(load_date));
                """,
    "base_repo": """
                create table if not exists bronze.base_repo (
                    stat_id BIGINT,
                    owner STRING,
                    repo STRING,
                    fork_count INT,
                    size_count INT,
                    watchers_count INT,
                    open_issues_count INT,
                    network_count INT,
                    stargazers_count INT,
                    subscribers_count INT,
                    created_at TIMESTAMP,
                    pushed_at TIMESTAMP,
                    updated_at TIMESTAMP,
                    response STRING,
                    load_date TIMESTAMP
                )
                using iceberg
                location '{}'
                partitioned by (days(load_date));
                """,
    "overall": """
                create table if not exists bronze.overall (
                    id STRING,
                    package STRING,
                    endpoint STRING,
                    category STRING,
                    date DATE,
                    downloads INT,
                    load_date TIMESTAMP
                )
                using iceberg
                location '{}'
                partitioned by (days(load_date));
                """,
}