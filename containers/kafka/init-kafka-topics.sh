#!/bin/bash

# blocks until kafka is reachable
kafka-topics --bootstrap-server kafka:29092 --list

echo -e 'Creating kafka topics'
kafka-topics --bootstrap-server kafka:29092 --create --if-not-exists --topic commits --replication-factor 1 --partitions 3
kafka-topics --bootstrap-server kafka:29092 --create --if-not-exists --topic issues --replication-factor 1 --partitions 3
kafka-topics --bootstrap-server kafka:29092 --create --if-not-exists --topic base_repo --replication-factor 1 --partitions 3
kafka-topics --bootstrap-server kafka:29092 --create --if-not-exists --topic languages --replication-factor 1 --partitions 3

echo -e 'Successfully created the following topics:'
kafka-topics --bootstrap-server kafka:29092 --list