FROM alpine:3.3
MAINTAINER Petr Lomakin <plomakin@mirantis.com>

ARG cf_commit_or_branch
RUN echo "ipv6" >> /etc/modules
RUN echo "http://dl-1.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories; \
    echo "http://dl-2.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories; \
    echo "http://dl-3.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories; \
    echo "http://dl-4.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories; \
    echo "http://dl-5.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories

RUN apk upgrade
RUN apk --update add vim git nfs-common python-software-properties build-essential libssl-dev libffi-dev python-dev sqlite wget

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN pip install virtualenv

RUN git clone https://github.com/MirantisWorkloadMobility/CloudFerry CloudFerry
WORKDIR /CloudFerry
RUN git checkout $cf_commit_or_branch

RUN pip install .
