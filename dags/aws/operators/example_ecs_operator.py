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
from datetime import timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.providers.amazon.aws.operators.ecs import ECSOperator
from airflow.utils.dates import days_ago

config = Variable.get("ecs_config", deserialize_json=True)
dag_id = os.path.basename(__file__).replace(".py", "")

default_args = {
    "owner": "example",
    "start_date": days_ago(2),
    "retries": 1,
    "retry_delay": timedelta(minutes=60),
    "retry_exponential_backoff": True,
}

with DAG(
    dag_id=dag_id,
    default_args=default_args,
    schedule_interval=None,
) as dag:
    ecs_task = ECSOperator(
        task_id="ecs_task",
        task_definition=config["task_definition"],
        cluster=config["cluster"],
        overrides=config["overrides"],
        launch_type=config["launch_type"],
        network_configuration=config["network_configuration"],
    )
