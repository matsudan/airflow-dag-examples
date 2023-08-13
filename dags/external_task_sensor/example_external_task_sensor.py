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
from airflow import DAG
from airflow.models.dag import get_last_dagrun
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.session import provide_session

with DAG(
    dag_id="example_external_task_sensor",
    start_date=pendulum.datetime(2023, 8, 1, tz="UTC"),
    schedule_interval=None,
    catchup=False,
    tags=["example"],
):
    # ExternalTaskSensor with different schedule interval.
    @provide_session
    def _get_logical_date_of_external_dag(logical_date, session):
        dag_last_run = get_last_dagrun(
            dag_id="example_external_task_sensor_target",
            session=session,
            include_externally_triggered=True
        )
        return dag_last_run.logical_date

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end", trigger_rule="none_failed_min_one_success")
    for i in range(5):
        # A task sensing sleep_no4 task that sleeps for 256 seconds exceeds the sensor timeout,
        # so the task is soft_fail.
        t1 = ExternalTaskSensor(
            task_id=f"sensor_no{i}",
            external_dag_id="example_external_task_sensor_target",
            external_task_id=f"sleep_no{i}",
            execution_date_fn=_get_logical_date_of_external_dag,
            soft_fail=True,
            poke_interval=30,
            mode="reschedule",
            check_existence=True,
            timeout=90,
        )
        start >> t1 >> end


with DAG(
    dag_id="example_external_task_sensor_target",
    start_date=pendulum.datetime(2023, 8, 1, tz="UTC"),
    schedule_interval=None,
    catchup=False,
    tags=["example"],
):
    start = EmptyOperator(task_id="start")
    trigger = TriggerDagRunOperator(
        task_id="trigger",
        trigger_dag_id="example_external_task_sensor",
    )
    end = EmptyOperator(task_id="end")
    for i in range(5):
        sleep_time = pow(4, i)
        t1 = BashOperator(task_id=f"sleep_no{i}", bash_command=f"sleep {sleep_time}")
        trigger >> t1 >> end
    start >> trigger
