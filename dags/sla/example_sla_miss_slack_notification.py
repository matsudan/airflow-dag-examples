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
import time

import pendulum
from airflow.decorators import dag, task
from libs.slack import post_sla_miss_to_slack


@dag(
    start_date=pendulum.datetime(2022, 5, 1, tz="UTC"),
    schedule="*/2 * * * *",
    catchup=False,
    sla_miss_callback=post_sla_miss_to_slack,
    tags=["example"],
)
def example_sla_miss_slack_notification():
    # An SLA miss occurs in this `sleep20_sla_miss` task, which is notified to slack.
    @task(sla=datetime.timedelta(seconds=5))
    def sleep20_sla_miss():
        time.sleep(20)

    @task(sla=datetime.timedelta(seconds=10))
    def sleep1():
        time.sleep(1)

    sleep20_sla_miss() >> sleep1()


dag = example_sla_miss_slack_notification()
