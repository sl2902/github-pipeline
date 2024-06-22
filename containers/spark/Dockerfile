# Use the Python 3.9 base image
# FROM python:3.9-bullseye
FROM tabulario/spark-iceberg:latest

# Install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      openjdk-11-jdk \
      openssh-server \
      sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt


# Environment variables for Spark and Iceberg
ENV SPARK_HOME="/opt/spark"
ENV APP_PATH=${SPARK_HOME}/kafka_consumer
ENV SPARK_VERSION="3.5.1"
ENV SPARK_MAJOR_VERSION="3.5"
ENV ICEBERG_VERSION="1.5.2"
ENV KAFKA_CLIENT_VERSION="0-10"
ENV PYTHONPATH="$SPARK_HOME:${APP_PATH}:$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip"
ENV PATH="$SPARK_HOME/sbin:$SPARK_HOME/bin:$PATH"
ENV SPARK_CONF_DIR="$SPARK_HOME/conf"
ENV PYSPARK_PYTHON="python3"

# Environment variable for Kafka
ENV BOOTSTRAP_SERVER=kafka:29092

# Set working directory
WORKDIR $SPARK_HOME


# Download and install Spark
RUN mkdir -p $SPARK_HOME && \
    curl -o spark-${SPARK_VERSION}-bin-hadoop3.tgz https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    tar -xvzf spark-${SPARK_VERSION}-bin-hadoop3.tgz --strip-components=1 && \
    rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

# Create SSH directory and configure SSH server
# RUN mkdir /var/run/sshd && \
# echo 'root:root' | chpasswd
# sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
# sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Create a new user 'spark_user' with sudo privileges
RUN useradd -ms /bin/bash spark_user && \
echo "spark_user:airflow" | chpasswd && \
usermod -aG sudo spark_user


# Download Iceberg Spark runtime, AWS bundle and Kafka
# RUN curl -o $SPARK_HOME/jars/iceberg-spark-runtime-${SPARK_MAJOR_VERSION}_2.12-${ICEBERG_VERSION}.jar \
#     https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-${SPARK_MAJOR_VERSION}_2.12/${ICEBERG_VERSION}/iceberg-spark-runtime-${SPARK_MAJOR_VERSION}_2.12-${ICEBERG_VERSION}.jar && \
#     curl -o $SPARK_HOME/jars/iceberg-aws-bundle-${ICEBERG_VERSION}.jar \
#     https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-aws-bundle/${ICEBERG_VERSION}/iceberg-aws-bundle-${ICEBERG_VERSION}.jar 
    # curl -o $SPARK_HOME/jars/spark-sql-kafka-${KAFKA_CLIENT_VERSION}_2.12-${SPARK_VERSION}.jar \
    # https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-${KAFKA_CLIENT_VERSION}_2.12/${SPARK_VERSION}/spark-sql-kafka-${KAFKA_CLIENT_VERSION}_2.12-${SPARK_VERSION}.jar
    # curl -o $SPARK_HOME/jars/aws-java-sdk-s3-1.12.630.jar \
    # https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-s3/1.12.630/aws-java-sdk-s3-1.12.630.jar

# Copy jars from local filesystem to avoid timeout which happen with the aws sdk bundle
# COPY jars/ ${SPARK_HOME}/jars

# Copy download jars script and execute it
# COPY download_jars.sh /tmp/download_jars.sh

# Make the script executable and run it
# RUN chmod +x /tmp/download_jars.sh && /tmp/download_jars.sh


# Create necessary directories
RUN mkdir -p /home/iceberg/localwarehouse /home/iceberg/warehouse /home/iceberg/spark-events /home/iceberg

# Copy configuration files
COPY .pyiceberg.yaml /root/.pyiceberg.yaml
COPY ./conf/spark-defaults.conf $SPARK_CONF_DIR/spark-defaults.conf

# Create event logging directory
RUN mkdir -p /tmp/spark-events /opt/spark/spark-events && chmod -R 777 /opt/spark/spark-events

# Create script directory
RUN mkdir -p /opt/spark/kafka_consumer

# Set permissions
RUN chmod u+x $SPARK_HOME/sbin/* && \
    chmod u+x $SPARK_HOME/bin/*

# Copy entrypoint script
COPY entrypoint.sh .
RUN chmod +x /opt/spark/entrypoint.sh

# Start SSH service
# CMD ["/usr/sbin/sshd", "-D"]

# Define the entrypoint
ENTRYPOINT ["./entrypoint.sh"]