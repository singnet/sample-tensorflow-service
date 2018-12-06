# example-service

[![CircleCI](https://circleci.com/gh/singnet/example-service.svg?style=svg)](https://circleci.com/gh/singnet/example-service)

Simple arithmetic service compatible with SingularityNET

## Getting Started

### Prerequisites

* [Python 3.6.5](https://www.python.org/downloads/release/python-365/)

### Installing

* Clone the git repository:

```
$ git clone git@github.com:singnet/example-service.git
$ cd example-service
```

* Install the dependencies and compile the protobuf file:

```
$ pip3 install -r requirements.txt
$ sh buildproto.sh
```

### Running

#### Standalone

* Run the example service directly (without `SNET Daemon`):

```
$ python3 run_example_service.py --no-daemon
```

* To test it run the script:

```
$ python3 test_example_service.py
```

#### With SingularityNET Daemon

##### SingularityNET Daemon Configuration

Now you must follow the [howToPublishService](https://github.com/singnet/wiki/tree/master/tutorials/howToPublishService)
tutorial to publish this service and set the `snetd.config.json` file.

Then, be sure that you have the `snetd` in your PATH.

Create the `snetd.config.json` file using this template:

```
{
   "DAEMON_END_POINT": "http://DAEMON_HOST:DAEMON_PORT",
   "ETHEREUM_JSON_RPC_ENDPOINT": "https://kovan.infura.io",
   "IPFS_END_POINT": "http://ipfs.singularitynet.io:80",
   "REGISTRY_ADDRESS_KEY": "0x2e4b2f2b72402b9b2d6a7851e37c856c329afe38",
   "PASSTHROUGH_ENABLED": true,
   "PASSTHROUGH_ENDPOINT": "http://SERVICE_GRPC_HOST:SERVICE_GRPC_PORT",  
   "ORGANIZATION_NAME": "ORGANIZATION_NAME",
   "SERVICE_NAME": "SERVICE_NAME",
   "LOG": {
       "LEVEL": "debug",
       "OUTPUT": {
            "TYPE": "stdout"
           }
   }
}
```

For example, replace tags with:

- `http://DAEMON_HOST:DAEMON_PORT`: http://54.203.198.53:7000
- `http://SERVICE_GRPC_HOST:SERVICE_GRPC_PORT`: http://localhost:7003
- `ORGANIZATION_NAME`: example-organization
- `SERVICE_NAME`: example-service

See [SingularityNet daemon configuration](https://github.com/singnet/snet-daemon/blob/master/README.md#configuration) for detailed configuration description.

##### Running Service + Daemon on Host

* Run the script without flag to launch both `SNET Daemon` and the service

```
$ python3 run_example_service.py
```

##### Running Service + Daemon in Docker Container

* Build the docker image and run a Container from it:

```
$ docker build -t snet_example_service https://github.com/singnet/example-service.git#master
$ docker run -p 7000:7000 -ti snet_example_service bash
```

From this point we follow the tutorial in the Docker Container's prompt.

After this, run the service (with `SNET Daemon`):

```
# python3 run_example_service.py &
```

### Testing

* Invoke the test script (from the same Docker Container):

```
# python3 test_example_service.py
```

## License

This project is licensed under the MIT License - see the
[LICENSE](https://github.com/singnet/example-service/blob/master/LICENSE) file for details.
