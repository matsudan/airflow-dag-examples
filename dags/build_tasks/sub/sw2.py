from airflow.operators.dummy_operator import DummyOperator


def build_tasks(dag):
    start = DummyOperator(task_id="start_sw2", dag=dag)
    end = DummyOperator(task_id="end_sw2", dag=dag)

    t1 = DummyOperator(
        task_id="task1_sw2",
        dag=dag,
    )

    start >> t1 >> end
    return (start, end)
