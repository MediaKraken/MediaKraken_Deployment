FROM ubuntu:16.04
ADD . /code
WORKDIR /code
RUN apt-get -y install python-pip && pip install -r requirements.txt
CMD python app.py
