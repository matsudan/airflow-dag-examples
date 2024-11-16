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
from airflow import DAG
from airflow.decorators import task
from airflow.timetables.trigger import CronTriggerTimetable

with DAG(
    dag_id="example_cron_trigger_timetable",
    start_date=pendulum.datetime(2024, 11, 1, tz="UTC"),
    schedule=CronTriggerTimetable("15 6 * * *", timezone="UTC"),  # run dag independent of data interval.
    catchup=False,
    tags=["time_table"],
):
    @task
    def print_date(date):
        print("date: ", date)

    # The value of logical_date will be the date of dag execution
    print_date("{{ ds }}")

    @task
    def print_data_interval(start, end):
        print("data_interval_start: ", start)
        print("data_interval_end: ", end)

    # The value of data_interval_start and data_interval_end will be the same, which is the date of dag execution
    print_data_interval(
        "{{ data_interval_start | ds }}",
        "{{ data_interval_start | ds }}"
    )
