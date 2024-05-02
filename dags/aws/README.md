## Setup for DAGs using AWS Operator/Hook

- Run [LocalStack](https://github.com/localstack/localstack) with docker

```shell
docker compose -f docker-compose.localstack.yaml up -d
```

### LocalStack

- Create S3 bucket

```shell
aws --endpoint-url=http://localhost:4566 s3 mb s3://<bucket>
```

- Create SNS topic

```shell
aws --endpoint-url=http://localhost:4566 sns create-topic --name <topic>
```

### Airflow

#### Variables

- sns_publish_config

```json
{
  "topic_arn": "YOUR_TOPIC_ARN"
}
```

#### Connection

- aws_default

| Command | Description |
| --- | --- |
| Conn Type | Amazon Web Service |
| HOST | |
| Schema | |
| Login | |
| Password| |
| Port| |
| Extra | {"aws_access_key_id": "YOUR_AWS_ACCESS_KEY", "aws_secret_access_key": "YOUR_SECRET_ACCESS_KEY", "region_name": "YOUR_REGION"} |
