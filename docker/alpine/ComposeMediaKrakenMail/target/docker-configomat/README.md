# docker-configomat

[![Build Status](https://img.shields.io/travis/alinmear/docker-configomat.svg?style=flat?branch=master)](https://travis-ci.org/alinmear/docker-configomat)
[![Github Stars](https://img.shields.io/github/stars/alinmear/docker-configomat.svg?style=flat)](https://github.com/alinmear/docker-configomat) 
[![Github Forks](https://img.shields.io/github/forks/alinmear/docker-configomat.svg?style=flat?label=github%20forks)](https://github.com/alinmear/docker-configomat/)
[![Gitter](https://img.shields.io/gitter/room/alinmear/docker-configomat.svg?style=flat)](https://gitter.im/alinmear/docker-configomat)

A simple shellscript to easily substitue config files based on env variables

This little project should make the configuration part of small docker projects easier. 

__NOTE__: 
* For now you must have the bash shell installed. Especially alpine is using `sh` by default (`apk add --no-update --no-cache bash`).
* `key=value` pairs without spaces are not supported at the moment (`key = value` is supported)

# Logics

Just define an env prefix, the key and the value of a config file:

`cat /etc/kopano/ical.cfg`:
```
[...]
# File with RSA key for SSL
ssl_private_key_file = /ssl/key.pem

# File with certificate for SSL
ssl_certificate_file = /ssl/cert.pem

# Verify client certificate
ssl_verify_client = no
[...]
```

```bash
export LDAP_SSL_PRIVATE_KEY_FILE=/tmp/test.pem
export LDAP_SSL_VERIFY_CLIENT=yes
configomat.sh LDAP_ /etc/kopano/ica.cfg
```

# Usage

```bash
configomat.sh <PREFIX> <FILE>
# or
confiromat.sh <PREFIX> "<FILE1> <FILE2> <FILE3>"
```

# Use within your docker project

* Add subproject
```bash
cd <your-project>
git add submodule https://github.com/alinmear/docker-configomat.git
git commit
```

* Extend your Dockerfile with theses lines
```bash
COPY docker-configomant/configomat.sh /usr/local/bin
RUN chmod +x /usr/local/bin/*
```

Now you can call the script within your other scripts like described above:
```bash
configomat.sh <PREFIX> <FILES>
```
