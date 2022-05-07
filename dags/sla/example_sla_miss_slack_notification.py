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

import datetime
import json
import time
from typing import Any, List

import pendulum
from airflow import DAG
from airflow.decorators import dag, task
from airflow.providers.http.operators.http import SimpleHttpOperator


def send_slack_notification(message: str, **context: Any):
    slack_notification = SimpleHttpOperator(
        task_id="sla_miss_notification",
        http_conn_id="slack_conn",  # The content of this connection is described in `sla/README.md`.
        endpoint="<Set your Slack Webhook URL>",  # e.g., "services/XXXXX/XXXXX/XXXXX"
        method="POST",
        data=message,
    )

    slack_notification.execute(context)


def sla_callback(
    dag: DAG, task_list: str, blocking_task_list: str, slas: List, blocking_tis: List
):
    text = (
        "SLA was missed on dag_id={dag_id}, "
        "task_id={task_id} on execution_date={execution_date}, "
        "task_instance={task_instance}".format(
            dag_id=dag.dag_id,
            task_id=slas[0].task_id,
            execution_date=slas[0].execution_date,
            task_instance=blocking_tis[0],
        )
    )

    message = json.dumps({"text": text})
    send_slack_notification(message)


@dag(
    start_date=pendulum.datetime(2022, 5, 1, tz="UTC"),
    schedule_interval="*/2 * * * *",
    catchup=False,
    sla_miss_callback=sla_callback,
    tags=["example"],
)
def example_sla_miss_slack_notification():

    # An SLA miss occurs in this `sleep20_sla_miss` task, which is notified to slack.
    @task(sla=datetime.timedelta(seconds=10))
    def sleep20_sla_miss():
        time.sleep(20)

    @task(sla=datetime.timedelta(seconds=10))
    def sleep1():
        time.sleep(1)

    sleep20_sla_miss() >> sleep1()


dag = example_sla_miss_slack_notification()
