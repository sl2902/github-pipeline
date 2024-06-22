FROM apache/airflow:2.8.1
# USER root

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#     curl \
#     default-jdk && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*
# USER airflow
# ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# USER airflow
# Create SSH keys
RUN ssh-keygen -t ecdsa -b 521 -f /home/airflow/.ssh/id_ecdsa -N ''
COPY requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION}  -r requirements.txt