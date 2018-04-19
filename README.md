# alpha-daemon

Simple image classification service for use with the alpha SingularityNET daemon

## Getting Started

These instructions are intended to act as a guide on how one may go about running a service on the SingularityNET alpha.

### Prerequisites

* [Docker](https://store.docker.com/search?type=edition&offering=community)

### Installing
* Clone the git repository
```bash
$ git clone git@github.com:singnet/alpha-service-example.git
$ cd alpha-service-example
```

* Update the snetd.config file (the following is for example purposes only)
```json
{
    "ETH_NODE_ENDPOINT": "https://kovan.infura.io",
    "AGENT_ADDRESS": "0x0000000000000000000000000000000000000000",
    "HDWALLET_MNEMONIC": "twelve-word mnemonic of the wallet the daemon should use for blockchain interactions",
    "HDWALLET_INDEX": 0,
    "PASSTHROUGH_ENABLED": true
}
```

* Build the docker image
```bash
$ docker build .
```

### Running
* Run the docker container
```bash
$ docker run --detach -p 5000:5000 service:latest
```

## License

This project is licensed under the MIT License - see the
[LICENSE](https://github.com/singnet/alpha-daemon/blob/master/LICENSE) file for details.
