import sys
import logging

import grpc
import concurrent.futures as futures

import service.common

# Importing the generated codes from buildproto.sh
import service.service_spec.example_service_pb2_grpc as grpc_bt_grpc
from service.service_spec.example_service_pb2 import Result

logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger("example_service")


"""
Simple arithmetic service to test the Snet Daemon (gRPC), dApp and/or Snet-CLI.
The user must provide the method (arithmetic operation) and
two numeric inputs: "a" and "b".

e.g:
With dApp:  'method': mul
            'params': {"a": 12.0, "b": 77.0}
Resulting:  response:
                value: 924.0


Full snet-cli cmd:
$ snet client call mul '{"a":12.0, "b":77.0}'

Result:
(Transaction info)
Signing job...

Read call params from cmdline...

Calling service...

    response:
        value: 924.0
"""


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class CalculatorServicer(grpc_bt_grpc.CalculatorServicer):
    def __init__(self):
        self.a = 0
        self.b = 0
        self.result = 0
        # Just for debugging purpose.
        log.debug("CalculatorServicer created")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def add(self, request, context):
        # In our case, request is a Numbers() object (from .proto file)
        self.a = request.a
        self.b = request.b

        # To respond we need to create a Result() object (from .proto file)
        self.result = Result()

        self.result.value = self.a + self.b
        log.debug("add({},{})={}".format(self.a, self.b, self.result.value))
        return self.result

    def sub(self, request, context):
        self.a = request.a
        self.b = request.b

        self.result = Result()
        self.result.value = self.a - self.b
        log.debug("sub({},{})={}".format(self.a, self.b, self.result.value))
        return self.result

    def mul(self, request, context):
        self.a = request.a
        self.b = request.b

        self.result = Result()
        self.result.value = self.a * self.b
        log.debug("mul({},{})={}".format(self.a, self.b, self.result.value))
        return self.result

    def div(self, request, context):
        self.a = request.a
        self.b = request.b

        self.result = Result()
        self.result.value = self.a / self.b
        log.debug("div({},{})={}".format(self.a, self.b, self.result.value))
        return self.result


# The gRPC serve function.
#
# Params:
# max_workers: pool of threads to execute calls asynchronously
# port: gRPC server port
#
# Add all your classes to the server here.
# (from generated .py files by protobuf compiler)
def serve(max_workers=10, port=7777):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    grpc_bt_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port("[::]:{}".format(port))
    return server


if __name__ == "__main__":
    """
    Runs the gRPC server to communicate with the Snet Daemon.
    """
    parser = service.common.common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    service.common.main_loop(serve, args)
