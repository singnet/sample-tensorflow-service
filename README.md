# example-service

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

* The following configuration values should be populated in a file (e.g. snetd.config) as described
```json
{
    "AGENT_CONTRACT_ADDRESS": "",
    "AUTO_SSL_DOMAIN": "",
    "AUTO_SSL_CACHE_DIR": "",
    "BLOCKCHAIN_ENABLED": true,
    "CONFIG_PATH": "",
    "DAEMON_LISTENING_PORT": 5000,
    "DAEMON_TYPE": "",
    "DB_PATH": "",
    "ETHEREUM_JSON_RPC_ENDPOINT": "",
    "EXECUTABLE_PATH": "",
    "HDWALLET_INDEX": 0,
    "HDWALLET_MNEMONIC": "",
    "LOG_LEVEL": 5,
    "PASSTHROUGH_ENABLED": true,
    "PASSTHROUGH_ENDPOINT": "",
    "POLL_SLEEP": "",
    "PRIVATE_KEY": "",
    "SERVICE_TYPE": "jsonrpc",
    "SSL_CERT": "",
    "SSL_KEY": "",
    "WIRE_ENCODING": "json"
}
```
* AGENT_CONTRACT_ADDRESS: the address of the Agent contract instance associated with this service (only applicable if
BLOCKCHAIN_ENABLED)
* AUTO_SSL_DOMAIN: domain for which daemon should acquire LetsEncrypt SSL certificates
* AUTO_SSL_CACHE_DIR: directory in which daemon should cache LetsEncrypt SSL certificates
* BLOCKCHAIN_ENABLED: whether the daemon validates and completes calls against the blockchain
* DAEMON_LISTENING_PORT: the port on which the daemon will listen for incoming JSON-RPC calls over http (must differ
from SERVER_PORT in the service configuration)
* DAEMON_TYPE: type of endpoint that daemon should expose; "http" for alpha-style JSON-RPC over HTTP proxy, "grpc" to
enable new gRPC features
* DB_PATH: path at which daemon should maintain local database of blockchain and job state
* ETHEREUM_JSON_RPC_ENDPOINT: the Ethereum node the daemon should run its blockchain client against (i.e. geth,
ganache, infura; only applicable if BLOCKCHAIN_ENABLED)
* EXECUTABLE_PATH: not used for example service
* HDWALLET_INDEX: the index of the account that the daemon should use to transact on the blockchain
* HDWALLET_MNEMONIC: the [bip39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) mnemonic corresponding
with the root seed for the [bip32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki) wallet from which
the daemon's account should be derived
* LOG_LEVEL: the logging verbosity of the daemon
* PASSTHROUGH_ENABLED: whether the daemon delegates calls to service or echoes requests back to the client (should be
true)
* PASSTHROUGH_ENDPOINT: the endpoint on which the service is configured to listen for incoming JSON-RPC calls over http
* POLL_SLEEP: time between checking blockchain state (defaults to 5s)
* PRIVATE_KEY: the hex-encoded private key for the account that the daemon should use to transact on the blockchain 
(takes precedence if both PRIVATE_KEY and HDWALLET_MNEMONIC are provided)
* SERVICE_TYPE: example service is "jsonrpc" service type
* SSL_CERT: path to certificate file daemon should use for SSL
* SSL_KEY: path to key file daemon should use for SSL
* WIRE_ENCODING: example service uses "json" wire encoding

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
