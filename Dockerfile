FROM python:3.6.5-stretch
ADD . /
RUN pip3 install -r /requirements.txt
RUN touch /snetd.config
CMD ["./scripts/run-snet-service"]
