#!/bin/bash

cd "$(git rev-parse --show-toplevel)"

echo "Adding connections"
# localstack
docker compose run --rm airflow-cli connections add \
  --conn-type "aws" \
  --conn-extra '{
        "aws_access_key_id": "dummy",
        "aws_secret_access_key": "dummy",
        "region_name": "ap-northeast-1",
        "endpoint_url": "http://localstack:4566"
    }' \
  aws_default

echo "Adding variables"
confs=$(ls config/)
for conf in $confs
do
  echo "${conf}"
  docker compose run --rm airflow-cli variables import "config/${conf}"
done
