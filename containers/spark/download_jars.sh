#!/bin/bash

# Define the SPARK_HOME directory
SPARK_HOME=${SPARK_HOME}

jars=(
    'jackson-annotations-2.14.2.jar::https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-annotations/2.14.2/jackson-annotations-2.14.2.jar'
    'jackson-core-2.14.2.jar::https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-core/2.14.2/jackson-core-2.14.2.jar'
    'jackson-databind-2.14.2.jar::https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-databind/2.14.2/jackson-databind-2.14.2.jar'
    'caffeine-2.9.3.jar::https://repo1.maven.org/maven2/com/github/ben-manes/caffeine/caffeine/2.9.3/caffeine-2.9.3.jar'
    'jsr305-3.0.0.jar::https://repo1.maven.org/maven2/com/google/code/findbugs/jsr305/3.0.0/jsr305-3.0.0.jar'
    'error_prone_annotations-2.10.0.jar::https://repo1.maven.org/maven2/com/google/errorprone/error_prone_annotations/2.10.0/error_prone_annotations-2.10.0.jar'
    'commons-logging-1.1.3.jar::https://repo1.maven.org/maven2/commons-logging/commons-logging/1.1.3/commons-logging-1.1.3.jar'
    'aircompressor-0.26.jar::https://repo1.maven.org/maven2/io/airlift/aircompressor/0.26/aircompressor-0.26.jar'
    'avro-1.11.3.jar::https://repo1.maven.org/maven2/org/apache/avro/avro/1.11.3/avro-1.11.3.jar'
    'commons-compress-1.22.jar::https://repo1.maven.org/maven2/org/apache/commons/commons-compress/1.22/commons-compress-1.22.jar'
    'commons-pool2-2.11.1.jar::https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar'
    'hadoop-client-api-3.3.4.jar::https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-client-api/3.3.4/hadoop-client-api-3.3.4.jar'
    'hadoop-client-runtime-3.3.4.jar::https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-client-runtime/3.3.4/hadoop-client-runtime-3.3.4.jar'
    'httpclient5-5.3.1.jar::https://repo1.maven.org/maven2/org/apache/httpcomponents/client5/httpclient5/5.3.1/httpclient5-5.3.1.jar'
    'httpcore5-5.2.4.jar::https://repo1.maven.org/maven2/org/apache/httpcomponents/core5/httpcore5/5.2.4/httpcore5-5.2.4.jar'
    'httpcore5-h2-5.2.4.jar::https://repo1.maven.org/maven2/org/apache/httpcomponents/core5/httpcore5-h2/5.2.4/httpcore5-h2-5.2.4.jar'
    'iceberg-api-1.5.2.jar::https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-api/1.5.2/iceberg-api-1.5.2.jar'
    'iceberg-aws-1.5.2.jar::https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-aws/1.5.2/iceberg-aws-1.5.2.jar'
    'iceberg-bundled-guava-1.5.2.jar::https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-bundled-guava/1.5.2/iceberg-bundled-guava-1.5.2.jar'
    'iceberg-common-1.5.2.jar::https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-common/1.5.2/iceberg-common-1.5.2.jar'
    'iceberg-core-1.5.2.jar::https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-core/1.5.2/iceberg-core-1.5.2.jar'
    'iceberg-spark-runtime-3.5_2.12-1.5.2.jar::https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.5.2/iceberg-spark-runtime-3.5_2.12-1.5.2.jar'
    'kafka-clients-3.4.1.jar::https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.4.1/kafka-clients-3.4.1.jar'
    'spark-sql-kafka-0-10_2.12-3.5.1.jar::https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.1/spark-sql-kafka-0-10_2.12-3.5.1.jar'
    'spark-token-provider-kafka-0-10_2.12-3.5.1.jar::https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.1/spark-token-provider-kafka-0-10_2.12-3.5.1.jar'
    'checker-qual-3.42.0.jar::https://repo1.maven.org/maven2/org/checkerframework/checker-qual/3.42.0/checker-qual-3.42.0.jar'
    'lz4-java-1.8.0.jar::https://repo1.maven.org/maven2/org/lz4/lz4-java/1.8.0/lz4-java-1.8.0.jar'
    'postgresql-42.7.3.jar::https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.3/postgresql-42.7.3.jar'
    'RoaringBitmap-1.0.1.jar::https://repo1.maven.org/maven2/org/roaringbitmap/RoaringBitmap/1.0.1/RoaringBitmap-1.0.1.jar'
    'slf4j-api-2.0.7.jar::https://repo1.maven.org/maven2/org/slf4j/slf4j-api/2.0.7/slf4j-api-2.0.7.jar'
    'snappy-java-1.1.10.3.jar::https://repo1.maven.org/maven2/org/xerial/snappy/snappy-java/1.1.10.3/snappy-java-1.1.10.3.jar'
)


# Loop through the jars array and download each file
echo "Length of array ${#jars[@]}"
for index in "${jars[@]}"; do
    FILENAME="${index%%::*}"
    VALUE="${index##*::}"
    
    echo "Downloading $FILENAME from $VALUE"
    curl -o "$SPARK_HOME/jars/$FILENAME" "$VALUE"
    
    if [ $? -ne 0 ]; then
        echo "Error downloading $FILENAME"
        exit 1
    fi
done

echo "All JARs downloaded successfully."

# ['org_apache_spark_spark-sql-kafka-0-10_2_12_3_5_1_jar']="https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.1/spark-sql-kafka-0-10_2.12-3.5.1.jar"
#     ['org_apache_spark_spark-token-provider-kafka-0-10_2_12_3_5_1_jar']="https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.1/spark-token-provider-kafka-0-10_2.12-3.5.1.jar"