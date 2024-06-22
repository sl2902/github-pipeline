#!/bin/bash

SPARK_WORKLOAD=$1
# Start the SSH server
#  /usr/sbin/sshd -D &
# sudo service ssh start
 sudo /etc/init.d/ssh start

echo "SPARK_WORKLOAD: $SPARK_WORKLOAD"
start-thriftserver.sh  --driver-java-options "-Dderby.system.home=/tmp/derby"

if [ "$SPARK_WORKLOAD" == "master" ];
then
  $SPARK_HOME/sbin/start-master.sh -p 7077
elif [ "$SPARK_WORKLOAD" == "worker" ];
then
  $SPARK_HOME/sbin/start-worker.sh spark://spark-master:7077
elif [ "$SPARK_WORKLOAD" == "history" ]
then
  $SPARK_HOME/sbin/start-history-server.sh
fi

# start-master.sh -p 7077
# start-worker.sh spark://spark-master:7077
# start-history-server.sh
# start-thriftserver.sh  --driver-java-options "-Dderby.system.home=/tmp/derby"

# # Entrypoint, for example notebook, pyspark or spark-sql
# if [[ $# -gt 0 ]] ; then
#     eval "$1"
# fi