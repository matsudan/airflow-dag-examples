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
from airflow.models import Variable
from airflow.providers.amazon.aws.operators.sns import SnsPublishOperator
from airflow.utils.dates import days_ago

dag_id = os.path.basename(__file__).replace(".py", "")

default_args = {
    "owner": "example",
    "start_date": days_ago(2),
}

with DAG(
    dag_id=dag_id,
    default_args=default_args,
    schedule=None,
) as dag:
    config = Variable.get("aws", deserialize_json=True)
    target_arn = config["sns"]["topic_arn"]
    publish = SnsPublishOperator(
        task_id="publish_test_topic",
        target_arn=target_arn,
        message="TEST",
    )
