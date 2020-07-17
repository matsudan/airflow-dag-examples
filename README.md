# airflow-dag-examples
This repository has some examples of Airflow DAGs and dockerized Airflow based on [docker-airflow](https://github.com/puckel/docker-airflow) by Puckel.
You can run the DAG examples on your local docker.
The DAG examples can be found in the `dags` directory.

## Requirements

* docker
* docker-compose

## Usage

1. Launch Airflow with LocalExecutor
```console
docker-compose up
```

2. Access the UI link `localhost:8080`
