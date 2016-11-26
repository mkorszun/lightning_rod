from python:2.7.12

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD celery -A application worker -B -l info -f /var/log/celery.log