[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/1lXY_Wlg)

# Tracking Trends in Python Package Usage and Repository Development

## Description
In today's data-rich environment, selecting the right datasets for analysis can be challenging. This project focuses on datasets from PyPI and the GitHub API, which will be stored, processed, and analyzed in a data warehouse. The objective is to build a robust pipeline to support an analytics framework capable of tracking trends in Python package usage and repository development. The analysis will cover the frequency of package downloads over time, version adoption rates, and user engagement metrics on PyPI, as well as repository activity metrics such as commit frequency, issue resolution times, and contributor trends on GitHub.

## Problem Description
Although GitHub and PyPI provide statistics about users' or organizations' repositories and Python packages, they lack comparative analysis across similar repositories and packages. For developers, maintainers, and stakeholders in the Python community, this project will help identify popular packages, active repositories, and overall trends in open source contributions. This data-driven approach will enhance decision-making processes, support better resource allocation, and foster a deeper understanding of the Python programming landscape.

## Conceptual Model
The primary datasets and APIs that will be used are the PyPI dataset from Google BigQuery and the GitHub API. This model will integrate data from these sources to provide comprehensive insights into Python package usage and repository development.

![conceptual_model](assets/conceptual_model_gh_pypi.png)

# High-level architecture
![High level architecture](assets/architecture.png)

# dbt Documentation
[View DBT Docs](https://sl2902.github.io/target/index.html)


# Datasource
The source of the data is GitHub Rest APIs. The following APIs are used:

- /repos/{owner}/{repo}/commits - List commits. Can query 5000 responses per hour
- /repos/{owner}/{repo}/issues - List issues in a repository. Only open issues will be listed. Can query 5000 responses per hour
- /repos/{owner}/{repo}/ - List summary statistics for a repository every day

# Metrics and Dashboard

Three repos were analyzed: Apache Iceberg, Apache Hudi and Delta-io Delta
<details>
<summary>Summary statistics for repos</summary>

- Provides a snapshot for various repository metrics such as fork_count, size, watchers_count, stargazers_count and subscribers_count

![summary stats](assets/summary_stats_repo.png)
</details>

<details>
<summary>Commits metrics</summary>
- A line chart comparing the three repositories by number of commits by authors for all time

![Count of author commits - all time](assets/count_author_commits_all_time.png)

- A line chart comparing the three repositories by number of commits by commiters for all time.

Note - Here the charts are almost identical as the commit_author_date nd commit_committer_date are identical when
the commiter is GitHub

![Count of commiter commits - all time](assets/count_committer_commits_all_time.png)

![Top 3 authors](assets/top3_authors_commits.png)

![Top 3 committers](assets/top3_committers_commits.png)
</details>

<details>
<summary>Issues metrics</summary>

- A line chart comparing the frequency of issues over time across the three repositories

![Count of issues - all time](assets/count_of_issues_all_time.png)

- A line chart showing the cumulative count of issues in the last 7 days

![Cumulative count of issues - last 7 days](assets/cumulative_count_of_issues_last_7_days.png)

- A line chart showing the number of days taken to update an issue

![Number of days taken to update an issue](assets/number_days_to_update_issues.png)

![Top 3 labels](assets/top3_labels.png)

</details>

<details>
<summary>PyPi packages metrics</summary>

- A line chart showing the percentage change in pyiceberg downloads - last 6 months

![Percent change pyiceberg downloads - last 6 months](assets/percentage_change_in_pyiceberg_downloads.png)

- A line chart showing the percentage change in delta-spark downloads - last 6 months

![Cumulative count of issues - last 7 days](assets/percentage_change_in_delta_spark_downloads.png)

</details>

# Dag dependencies
![Dag dependencies](assets/dag_dependencies.png)


# URLs and port numbers
| Service Name       | URL                   | Port | User   | Password |
|--------------------|-----------------------|------| -------|----------|
| Spark Master       | http://localhost:4040 | 4040 |        |          |
| Spark History      | http://localhost:18080| 18080|        |          |
| MinIO              | http://localhost:9000 | 9000 | minio  | minio123 |
| Airflow Webserver  | http://localhost:8080 | 8080 | airflow| airflow  |
| Trino              | http://localhost:1080 | 1080 | admin  |          |
| Streamlit          | http://localhost:8501 | 8501 |        |          |


# Steps to reproduce
**1.** Prerequisites:

<details>
<summary>Install Git for your OS</summary>
Installation instructions [here](https://git-scm.com/downloads)

You will need your Personal Access Token (PAT). For this, got the following page
and generate your PAT. Grant it the appropriate persmissions

[Generate PAT](https://github.com/settings/tokens)
</details>

Note - If you have already done these steps then it is not required. However, you will need the Personal Access Token (PAT)

<details>
<summary>Install Docker for your OS</summary>

Installation instructions[here](https://docs.docker.com/engine/install/)

Note - If you have already done these steps then it is not required.
</details>

**2.** Clone the repository:
```shell
git clone https://github.com/DataExpert-ZachWilson-V4/capstone-project-sundeep.git
```

**3.** Change the working directory:
```shell
cd capstone-project-sundeep/
```

**4.** Rename the env.template file to `.env`:
```shell
mv env.template .env
```

4.1 Fill in the blanks to the following environment variables in the `.env` file and save them:
```shell
GIT_PAT=
```

**5.** Load environment variables into the project directory:
```shell
source .env
```

**6.** Build Docker images:
```shell
make docker_build
```

6.1 Start Docker containers:
```shell
make docker_up
```

**7.** Create SSH connection for Spark job:
```shell
make ssh_conn
```

7.1 Run `base_repo` pipeline:
```shell
make dag_run_base_repo_pipeline
```

7.2 Run `commits` pipeline:
```shell
make dag_run_commits_pipeline
```

7.3 Run `issues` pipeline:
```shell
make dag_run_issues_pipeline
```

7.4 Launch Streamlit dashboard:
```shell
 http://localhost:8501
 ```





