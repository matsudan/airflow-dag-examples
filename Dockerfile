FROM puckel/docker-airflow:latest
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt