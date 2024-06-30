catalog = "iceberg"
schema = "bronze"

all_time_issues_trend = f"""
        select
            repo,
            created_at,
            num_issues
        from
            {catalog}.{schema}.fct_all_time_issues_trend
        """

last_7_days_fct_issues = f"""
        select 
            repo,
            created_at,
            issue_count
        from 
            {catalog}.{schema}.fct_last_7_days_fct_issues 
        """

num_updated_issues = f"""
        select
            repo,
            num_days,
            num_issues
        from
            {catalog}.{schema}.fct_num_updated_issues
        """

num_labels_per_repo = f"""
        select
            repo,
            label,
            num_labels
        from
            {catalog}.{schema}.fct_num_labels_per_repo
        """

all_time_author_commits_trend = f"""
        select
            repo,
            commit_author_date,
            num_commits
        from
            {catalog}.{schema}.fct_all_time_author_commits_trend
        """

all_time_committer_commits_trend = f"""
        select
            repo,
            commit_committer_date,
            num_commits
        from
            {catalog}.{schema}.fct_all_time_committer_commits_trend
        """

num_author_commits_by_repo = f"""
        select
            repo,
            author_name,
            num_commits
        from
            {catalog}.{schema}.fct_num_author_commits_by_repo
        """

num_committer_commits_by_repo = f"""
        select
            repo,
            committer_name,
            num_commits
        from
            {catalog}.{schema}.fct_num_committer_commits_by_repo
        """

summary_stats_base_repo = f"""
        select
            repo,
            owner,
            fork_count,
            size_count,
            watchers_count,
            open_issues_count,
            network_count,
            stargazers_count,
            subscribers_count
        from
            {catalog}.{schema}.fct_all_time_base_repo_stats
        """