topic_keys = {
    "commits": {
        "primary_key": "commit_sha",
        "partition_keys": ["repo", "commit_author_date"]
    },
    "issues": {
        "primary_key": "id",
        "partition_keys": ["repo", "created_at"]
    },
    "base_repo": {
        "primary_key": "stat_id",
        "partition_keys": ["repo", "updated_at"]
    }
}