# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbase_alpinepy3:dev

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the broadcast server"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken

WORKDIR /mediakraken

RUN pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && rm requirements.txt

# Copy the source files for the app
COPY src /mediakraken

EXPOSE 9101

CMD ["/bin/ash"]
