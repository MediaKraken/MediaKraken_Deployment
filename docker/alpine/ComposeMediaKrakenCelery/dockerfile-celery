FROM python:3.5-slim

WORKDIR /opt/module

ENV CELERY_VERSION 4.0.0rc7

RUN pip install celery=="$CELERY_VERSION"

ENV CELERY_BROKER_URL amqp://guest@rabbit

ENV C_FORCE_ROOT=true

CMD [ "celery", "worker" ]
