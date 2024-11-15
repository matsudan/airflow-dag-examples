#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import pendulum
from airflow import DAG, Dataset
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

example_dataset = Dataset("s3://dataset/example.csv")

with DAG(
    dag_id="example_dataset_producer",
    start_date=pendulum.datetime(2023, 3, 1, tz="UTC"),
    schedule=None,
    tags=["dataset"],
):
    # `example_dataset` may be updated by this upstream producer task.
    t1 = EmptyOperator(
        task_id="producer",
        outlets=[example_dataset],
    )

    # `example_dataset_consumer` DAG is executed before this `wait` task is completed.
    t2 = BashOperator(
        task_id="wait",
        bash_command="sleep 10",
    )

    t1 >> t2


# This DAG is triggered when `producer` task of `example_dataset_producer` DAG is completed successfully.
with DAG(
    dag_id="example_dataset_consumer",
    start_date=pendulum.datetime(2023, 3, 1, tz="UTC"),
    schedule=[
        example_dataset
    ],  # DAG can also require multiple datasets. e.g., [dataset1, dataset2]
    tags=["dataset"],
):
    EmptyOperator(task_id="consumer")
