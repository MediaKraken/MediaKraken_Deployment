FROM  mediakraken/mkbaseffmpeg:latest

RUN addgroup -g 1000 node \
    && adduser -u 1000 -G node -s /bin/sh -D node \
    && apk add --update --no-cache \
        nodejs \
        npm \
        yarn \
    && rm -rf /var/cache/apk/*

CMD [ "node" ]
