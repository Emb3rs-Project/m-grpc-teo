import os
from concurrent import futures

import dotenv
import grpc
import jsonpickle

from module.module.src.integration import run_build_model

from teo.teo_pb2 import BuildModelInput, BuildModelOutput
from teo.teo_pb2_grpc import TEOModuleServicer



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