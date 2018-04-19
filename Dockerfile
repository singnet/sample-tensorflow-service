FROM python:3.6.5-stretch
ADD . /service
RUN pip3 install -r /service/requirements.txt
CMD ["/service/scripts/example-service"]
