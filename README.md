# example-service

[![CircleCI](https://circleci.com/gh/singnet/example-service.svg?style=svg)](https://circleci.com/gh/singnet/example-service)

Simple image classification service compatible with the SingularityNET daemon

## Getting Started

### Prerequisites

* [Python 3.6.5](https://www.python.org/downloads/release/python-365/)

### Installing

* Clone the git repository
```bash
$ git clone git@github.com:singnet/example-service.git
$ cd example-service
```

* Install the dependencies
```bash
$ pip install -r requirements.txt
```

### Configuration

* The following default configuration can be overridden by populating configuration/config.json in the source tree with
the desired values
```json
{
  "SERVER_PORT": 5001,
  "MINIMUM_SCORE": 0.20,
  "LOG_LEVEL": 10
}
```
* SERVER_PORT: the port on which the example service will listen for incoming JSON-RPC calls over http
* MINIMUM_SCORE: the minimum confidence score (between 0 and 1 inclusive) required to return a given prediction
* LOG_LEVEL: the logging verbosity

### Running

#### Standalone

* Invoke the example service directly
```bash
$ python image_classification_service
```

#### With SingularityNET Daemon

##### SingularityNET Daemon Configuration

Create `snetd.config.json` file containing the following:
```json
{
  "passthrough_enabled": true
}
```
in order to enable example service work with daemon. See [SingularityNet daemon configuration](https://github.com/singnet/snet-daemon/blob/master/README.md#configuration) for detailed configuration description.

##### Running Service + Daemon on Host

* Invoke the run-snet-service script which launches both snetd and the example service
```bash
$ ./scripts/run-snet-service
```

##### Running Service + Daemon in Docker Container

* Ensure that PASSTHROUGH_ENDPOINT is configured to be "http://127.0.0.1:5001" in your daemon configuration
* Run the docker image with your daemon configuration (where HOST_PORT is the port you want the daemon bound to on your
host)
```bash
$ docker run --detach -p HOST_PORT:DAEMON_LISTENING_PORT -v /path/to/config:/snetd.config singularitynet/example-service:latest
```

### Testing

* Invoke the test-call script against a running instance of the example service
```bash
$ ./scripts/test-call
```

### Building Docker Image

* Invoke the docker build script
```bash
$ ./scripts/build-docker
```

## License

This project is licensed under the MIT License - see the
[LICENSE](https://github.com/singnet/example-service/blob/master/LICENSE) file for details.
