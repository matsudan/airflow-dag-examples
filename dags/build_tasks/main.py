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

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from build_tasks.sub.sw1 import build_tasks as sw1_build_tasks
from build_tasks.sub.sw2 import build_tasks as sw2_build_tasks
from build_tasks.sub.sw3 import build_tasks as sw3_build_tasks

default_args = {
    "owner": "example",
    "provide_context": True,
    "start_date": days_ago(2),
}

with DAG(
    dag_id="build_tasks_main",
    default_args=default_args,
    schedule_interval="@once",
) as dag:
    start = DummyOperator(task_id="start")

    start_sw1, end_sw1 = sw1_build_tasks(dag)
    start_sw2, end_sw2 = sw2_build_tasks(dag)
    start_sw3, end_sw3 = sw3_build_tasks(dag)

    # dependencies
    start >> [start_sw1, start_sw2]
    [end_sw1, end_sw2] >> start_sw3
