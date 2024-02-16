from dataclasses import dataclass
from functools import wraps

import requests
from airflow import DAG
from airflow.models import Variable


@dataclass
class SlackMessageConfig:
    color: str
    text: str
    attachment_text: str


def post_to_slack(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        c = func(*args, **kwargs)
        config = Variable.get("slack", deserialize_json=True)

        requests.post(
            config.get("webhook_url"),
            json={
                "blocks": [
                    {"type": "section", "text": {"type": "mrkdwn", "text": c.text}}
                ],
                "attachments": [
                    {
                        "color": c.color,
                        "blocks": [
                            {
                                "type": "section",
                                "text": {"type": "mrkdwn", "text": c.attachment_text},
                            }
                        ],
                    }
                ],
            },
        )

    return wrapper


@post_to_slack
def post_sla_miss_to_slack(
    dag: DAG, task_list: str, blocking_task_list: str, slas: list, blocking_tis: list
) -> SlackMessageConfig:

    return SlackMessageConfig(
        "#ffa500",
        f"@channel SLA was missed on {dag.dag_id}.\n",
        f"Task ID: {slas[0].task_id}\n" f"TaskInstance ID: {blocking_tis[0]}\n",
    )


@post_to_slack
def post_failure_to_slack(context: dict) -> SlackMessageConfig:

    return SlackMessageConfig(
        "#ff0000",
        f"@channel Task has failed on {context.get('task_instance').dag_id}.\n",
        (
            f"Task ID: {context.get('task').task_id}\n"
            f"Execution time: {context.get('logical_date')}\n"
            f"Reason: {context.get('reason')}\n"
            f"Log URL: {context.get('task_instance').log_url}\n"
        ),
    )
