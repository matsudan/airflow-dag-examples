#!/bin/bash

echo 'Create S3 bucket'
aws --endpoint-url=http://localhost:4566 s3 mb s3://sample-bucket

echo 'Create SNS topic'
aws --endpoint-url=http://localhost:4566 sns create-topic --name sample-topic --region ap-northeast-1
