#!/bin/bash
until /usr/bin/mc config host add myminio http://minio:9000 minio minio123; do
    echo '...waiting...'
    sleep 1
done
/usr/bin/mc rm -r --force myminio/gh-app 2> /dev/null
/usr/bin/mc mb myminio/gh-app
/usr/bin/mc policy download myminio/gh-app
/usr/bin/mc rm -r --force myminio/lakehouse 2> /dev/null
/usr/bin/mc mb myminio/lakehouse
/usr/bin/mc policy download myminio/lakehouse
exit 0