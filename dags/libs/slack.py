import requests
from airflow import DAG
from airflow.models import Variable


def _post_to_slack(color: str, text: str, attachment_text: str) -> None:
    config = Variable.get("slack", deserialize_json=True)

    requests.post(
        config["webhook_url"],
        json={
            "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": text}}],
            "attachments": [
                {
                    "color": color,
                    "blocks": [
                        {
                            "type": "section",
                            "text": {"type": "mrkdwn", "text": attachment_text},
                        }
                    ],
                }
            ],
        },
    )


def post_sla_miss_to_slack(
    dag: DAG, task_list: str, blocking_task_list: str, slas: list, blocking_tis: list
) -> None:

    att_text = (
        f"Task ID: {slas[0].task_id}\n"
        f"TaskInstance ID: {blocking_tis[0]}\n"
    )

    _post_to_slack(
        "#ffa500",
        f"@channel SLA was missed on {dag.dag_id}.\n",
        att_text,
    )
