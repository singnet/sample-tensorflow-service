FROM python:3.6.5-stretch
ADD . /service
RUN pip3 install -r /service/requirements.txt
RUN pip install /service/singularitynet_daemon-1.0.tar.gz
CMD ["/service/scripts/example_service"]
