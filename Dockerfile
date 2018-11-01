FROM python:3.6.5-stretch
ADD . /
RUN pip3 install -r /requirements.txt
RUN touch /snetd.config.json
RUN apt-get install -y wget
RUN wget https://github.com/singnet/snet-daemon/releases/download/v0.1.1/snetd-0.1.1.tar.gz
RUN tar -xvf snetd-0.1.1.tar.gz
CMD ["./scripts/run-snet-service"]
