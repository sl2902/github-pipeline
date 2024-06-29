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
<iframe src="https://sl2902.github.io/target/index.html" width="100%" height="600px"> </iframe>


# Datasource
The source of the data is GitHub Rest APIs. The following APIs are used:

- /repos/{owner}/{repo}/commits - List commits. Can query 5000 responses per hour
- /repos/{owner}/{repo}/issues - List issues in a repository. Only open issues will be listed. Can query 5000 responses per hour
- /repos/{owner}/{repo}/ - List summary statistics for a repository.


# URL and port
| Service Name       | URL                   | Port |
|--------------------|-----------------------|------|
| Spark Master       | http://localhost:4040 | 4040 |
| Spark History      | http://localhost:18080| 18080|
| MinIO              | http://localhost:9000 | 9000 |
| Airflow Webserver  | http://localhost:8080 | 8080 |
| Trino              | http://localhost:1080 | 1080 |
| Streamlit          | http://localhost:8501 | 8501 |


# Steps to reproduce
**1.** Prerequisites:

<details>
<summary>Install Git for your OS</summary>
Installation instructions [here](https://git-scm.com/downloads)

You will need your Personal Access Token (PAT). For this, got the following page
and generate your PAT. Grant it the appropriate persmissions

[Generate PAT](https://github.com/settings/tokens)
</details>

Note - If you have already done these steps then it is not required.

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





