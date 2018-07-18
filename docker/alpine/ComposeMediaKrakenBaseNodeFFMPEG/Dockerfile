FROM  mediakraken/mkbaseffmpeg:latest

RUN addgroup -g 1000 node \
    && adduser -u 1000 -G node -s /bin/sh -D node \
    && apk add --no-cache \
        nodejs \
        npm \
        yarn

CMD [ "node" ]
