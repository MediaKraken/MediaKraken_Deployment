FROM debian:jessie
MAINTAINER Benoît Vidis

ENV EDITOR=vim
ENV TERM=xterm-color

RUN apt-get update && apt-get install -y locales && locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8 

ADD https://www.deb-multimedia.org/pool/main/d/deb-multimedia-keyring/deb-multimedia-keyring_2016.8.1_all.deb /root/
RUN echo "deb http://www.deb-multimedia.org jessie main non-free" >> /etc/apt/sources.list && \
    dpkg -i /root/deb-multimedia-keyring_2016.8.1_all.deb && \
    apt-get update && \
    apt-get install -y \
        abcde \
        eyed3 \
        flac \
        id3 \
        nano \
        lame \
        python \
        vim && \
    mkdir -p /abcde/out && \
    echo "syntax on\nset expandtab ts=4 sw=4 autoindent encoding=utf8" >> etc/vim/vimrc

ADD abcde.conf /etc/abcde.conf


ENTRYPOINT [ "abcde" ]
