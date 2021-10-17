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

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup

dag_id = os.path.basename(__file__).replace(".py", "")

default_args = {
    "owner": "example",
    "start_date": days_ago(2),
}

with DAG(
    dag_id=dag_id,
    default_args=default_args,
    schedule_interval=None,
) as dag:
    start = DummyOperator(task_id="start")

    with TaskGroup(group_id="group1") as tg1:
        t1 = DummyOperator(task_id="task1")
        t2 = DummyOperator(task_id="task2")

        t1 >> t2

    with TaskGroup(group_id="group2") as tg2:
        t3 = DummyOperator(task_id="task3")

        # Define sub task group
        with TaskGroup(group_id="group2_1") as tg2_1:
            t4 = DummyOperator(task_id="task4")
            t5 = DummyOperator(task_id="task5")

            t4 >> t5

        with TaskGroup(group_id="group3_1") as tg3_1:
            for i in range(1, 3):
                tn = DummyOperator(task_id=f"task_tg3_{i}")

            t5 >> tn

        t3 >> tg2_1 >> tg3_1

    end = DummyOperator(task_id="end")

    start >> tg1 >> tg2 >> end
