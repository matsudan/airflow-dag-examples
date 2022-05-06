from typing import Tuple

from airflow import DAG
from airflow.models.baseoperator import BaseOperator
from airflow.operators.empty import EmptyOperator


def build_tasks(dag: DAG) -> Tuple[BaseOperator, BaseOperator]:
    start = EmptyOperator(task_id="start_sw3", dag=dag)
    end = EmptyOperator(task_id="end_sw3", dag=dag)

    t1 = EmptyOperator(
        task_id="task1_sw3",
        dag=dag,
    )
    t2 = EmptyOperator(
        task_id="task2_sw3",
        dag=dag,
    )

    start >> t1 >> t2 >> end
    return start, end
