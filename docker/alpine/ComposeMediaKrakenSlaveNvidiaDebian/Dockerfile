# Download base image
FROM mediakraken/mkbaseffmpegnvidiadebian

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the main slave app"

# create work dir
RUN mkdir /mediakraken

# copy PIP requirements
ADD requirements.txt /mediakraken
WORKDIR /mediakraken

RUN apt-get update \
  && apt-get -y install \
  python \
  python-pip \
  && pip install -r requirements.txt \
  && rm requirements.txt \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Copy the source files for the app
ADD src /mediakraken

CMD ["bash"]
