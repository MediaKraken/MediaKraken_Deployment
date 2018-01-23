FROM jenkins/jenkins:lts
USER root
RUN apt-get update && apt-get install -y python-pip sloccount
ADD requirements.txt /
RUN pip install -r /requirements.txt
USER jenkins
