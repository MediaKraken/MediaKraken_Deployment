FROM alpine:3.5
RUN apk add --no-cache python3 && python3 -m ensurepip
RUN pip3 install flower==0.9.1 celery==4.0.2 && rm -rf ~/.cache
EXPOSE 5555
ENTRYPOINT ["flower"]
