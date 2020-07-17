## Variables

### sns_publish_config
```json
{
  "topic_arn": "YOUR_TOPIC_ARN"
}
```

### ecs_config
```json
{
    "task_definition": "sample-def-mtd:2",
    "cluster": "airflow-task-proc",
    "overrides": {
        "containerOverrides": [
            {
                "name": "sample-con",
                "cpu": 256,
                "memory": 1024
            }
        ]
    },
    "launch_type": "FARGATE",
    "network_configuration": {
        "awsvpcConfiguration": {
            "subnets": ["subnet-xxxxxxxxxx"],
            "securityGroups": ["sg-xxxxxxx"]
        }
    }
}
```

## Connection

### aws_default
| Command | Description |
| --- | --- |
| Conn Type | Amazon Web Service |
| HOST | |
| Schema | |
| Login | |
| Password| |
| Port| |
| Extra | {"aws_access_key_id": "YOUR_AWS_ACCESS_KEY", "aws_secret_access_key": "YOUR_SECRET_ACCESS_KEY", "region_name": "YOUR_REGION"} |