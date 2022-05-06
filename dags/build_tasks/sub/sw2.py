from typing import Tuple

from airflow import DAG
from airflow.models.baseoperator import BaseOperator
from airflow.operators.empty import EmptyOperator


def build_tasks(dag: DAG) -> Tuple[BaseOperator, BaseOperator]:
    start = EmptyOperator(task_id="start_sw2", dag=dag)
    end = EmptyOperator(task_id="end_sw2", dag=dag)

    t1 = EmptyOperator(
        task_id="task1_sw2",
        dag=dag,
    )

    start >> t1 >> end
    return start, end
