topic_keys = {
    "commits": {
        "primary_key": "commit_sha",
        "partition_keys": ["repo", "load_date"]
    },
    "issues": {
        "primary_key": "id",
        "partition_keys": ["repo", "load_date"]
    },
    "base_repo": {
        "primary_key": "stat_id",
        "partition_keys": ["repo", "load_date"]
    },
    "overall": {
        "primary_key": "id",
        "partition_keys": ["load_date"]
    }
}