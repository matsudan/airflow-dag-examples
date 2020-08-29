from airflow.operators.dummy_operator import DummyOperator


def build_tasks(dag):
    start = DummyOperator(task_id="start_sw3", dag=dag)
    end = DummyOperator(task_id="end_sw3", dag=dag)

    t1 = DummyOperator(
        task_id="task1_sw3",
        dag=dag,
    )
    t2 = DummyOperator(
        task_id="task2_sw3",
        dag=dag,
    )

    start >> t1 >> t2 >> end
    return (start, end)
