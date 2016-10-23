FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r ../../pipeline-source/pipeline-build-os-pip-slave-ubuntu-1604.txt
CMD python app.py
