FROM ubuntu:18.04

ENV SINGNET_REPOS=/opt/singnet

RUN mkdir -p ${SINGNET_REPOS}

RUN apt-get update && \
    apt-get install -y \
    apt-utils \
    nano \
    git \
    wget \
    curl \
    zip \
    libudev-dev \
    libusb-1.0-0-dev

RUN apt-get install -y nodejs npm
RUN apt-get install -y python3 python3-pip

RUN cd ${SINGNET_REPOS} && \
    git clone https://github.com/singnet/snet-cli && \
    cd snet-cli && \
    ./scripts/blockchain install && \
    pip3 install -e .

RUN cd ${SINGNET_REPOS} && \
    mkdir snet-daemon && \
    cd snet-daemon && \
    wget https://github.com/singnet/snet-daemon/releases/download/v0.1.3/snetd-0.1.3.tar.gz && \
    tar -xvf snetd-0.1.3.tar.gz && \
    mv linux-amd64/snetd /usr/bin/snetd

RUN cd ${SINGNET_REPOS} && \
    git clone https://github.com/singnet/example-service.git && \
    cd example-service && \
    sh buildproto.sh

WORKDIR ${SINGNET_REPOS}/example-service
