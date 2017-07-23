# Download base image
FROM mediakraken/mkbaseffmpegnvidiadebian

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the main slave app"

# don't create /mediakraken as it's in the base image

# copy PIP requirements
ADD requirements.txt /mediakraken
WORKDIR /mediakraken

RUN apt-get update \
  && apt-get install \
  python \
  && pip install -r requirements.txt \
  && rm requirements.txt \

# Copy the source files for the app
ADD src /mediakraken

CMD ["bash"]
