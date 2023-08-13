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

import os

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

dag_id = os.path.basename(__file__).replace(".py", "")

with DAG(
    dag_id=dag_id,
    start_date=pendulum.datetime(2022, 5, 1, tz="UTC"),
    schedule_interval=None,
    tags=["example"],
) as dag:
    start = EmptyOperator(task_id="start")

    t1 = BashOperator.partial(task_id="dtm_task").expand(
        bash_command=["echo 1", "echo 2"]
    )

    # This task will be skipped.
    t2 = BashOperator.partial(task_id="dtm_skip_task").expand(bash_command=[])

    end = EmptyOperator(task_id="end", trigger_rule="none_failed")

    start >> t1 >> t2 >> end
