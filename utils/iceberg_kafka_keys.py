topic_keys = {
    "commits": {
        "primary_key": "commit_sha",
        "partition_keys": ["owner", "days(commit_author_date)"]
    },
    "issues": {
        "primary_key": "id",
        "partition_keys": ["owner", "days(created_at)"]
    },
    "base_repo": {
        "primary_key": "stat_id",
        "partition_keys": ["owner", "days(updated_at)"]
    }
}