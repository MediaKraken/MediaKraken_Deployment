# docker-debian-cuda - Debian 9 with CUDA Toolkit 8.0

FROM debian:stretch

# install from debian repositories
ENV DEBIAN_FRONTEND noninteractive
RUN echo 'Acquire::Retries "5";' > /etc/apt/apt.conf.d/99AcquireRetries \
 && sed -i 's/main$/main contrib non-free/' /etc/apt/sources.list \
 && apt-get update -qq \
 && apt-get install --no-install-recommends -y \
    gnupg2 \
    nvidia-cuda-toolkit \
    nvidia-smi \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
