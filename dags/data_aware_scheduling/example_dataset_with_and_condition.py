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

example_dataset1 = Dataset("s3://dataset1/and.csv")
example_dataset2 = Dataset("s3://dataset2/and.csv")

with DAG(
    dag_id="example_dataset_producer_with_and_condition",
    start_date=pendulum.datetime(2024, 11, 1, tz="UTC"),
    schedule=None,
    tags=["dataset"],
):
    start = EmptyOperator(task_id="start")

    # `example_dataset1` may be updated by this upstream producer task.
    t1 = BashOperator(
        task_id="wait5",
        bash_command="sleep 5",
        outlets=[example_dataset1],
    )

    # `example_dataset_consumer_with_and_condition` DAG is not executed before this `wait15` task is completed.
    t2 = BashOperator(
        task_id="wait15",
        bash_command="sleep 15",
        outlets=[example_dataset2],
    )

    start >> [t1, t2]


# This DAG is triggered when `wait15` task of `example_dataset_producer_with_and_condition` DAG is completed successfully.
with DAG(
    dag_id="example_dataset_consumer_with_and_condition",
    start_date=pendulum.datetime(2024, 11, 1, tz="UTC"),
    schedule=(example_dataset1 & example_dataset2),
    tags=["dataset"],
):
    EmptyOperator(task_id="consumer")
