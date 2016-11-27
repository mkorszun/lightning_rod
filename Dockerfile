from python:2.7.12

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
ENV C_FORCE_ROOT true
CMD celery -A application worker -B -l info -f /var/log/celery.log