import os
from concurrent import futures

import dotenv
import grpc
import jsonpickle

from teo.teo_pb2 import BuildModelInput, BuildModelOutput
from teo.teo_pb2_grpc import TEOModuleServicer, add_TEOModuleServicer_to_server

from module.module.src.integration import run_build_model


dotenv.load_dotenv()


class TEOModule(TEOModuleServicer):

  def __init__(self) -> None:
      pass

  def buildmodel(self, request : BuildModelInput, context) -> BuildModelOutput:
      input_dict = {
        "platform" : jsonpickle.decode(request.platform),
        "gis-module" : jsonpickle.decode(request.gis_module),
        "cf-module" : jsonpickle.decode(request.cf_module)
      }
      result = run_build_model(input_data=input_dict)

      return BuildModelOutput(
        output = jsonpickle.encode(result, unpicklable=True)
      )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_TEOModuleServicer_to_server(TEOModule(), server)

    server.add_insecure_port(
        f"{os.getenv('GRPC_HOST')}:{os.getenv('GRPC_PORT')}")

    print(
        f"TEO module Listening at {os.getenv('GRPC_HOST')}:{os.getenv('GRPC_PORT')}")

    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()