# -*- coding: utf-8 -*-
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

import os
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

dag_id = os.path.basename(__file__).replace(".py", "")

default_args = {
    "owner": "example",
    "start_date": datetime(2022, 5, 1),
}

with DAG(
    dag_id=dag_id,
    default_args=default_args,
    schedule_interval=None,
) as dag:

    t1 = EmptyOperator(task_id="task1")

    t2_1 = BashOperator.partial(task_id="dtm_task2_1").expand(
        bash_command=["echo 1", "echo 2"]
    )

    # This task will be skipped.
    t2_2 = BashOperator.partial(task_id="dtm_task2_2").expand(bash_command=[])

    t3 = EmptyOperator(task_id="task3", trigger_rule="none_failed")

    t1 >> [t2_1, t2_2] >> t3
