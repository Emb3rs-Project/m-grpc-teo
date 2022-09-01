import json
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
    def buildmodel(self, request: BuildModelInput, context) -> BuildModelOutput:
        input_dict = {
            "platform": jsonpickle.decode(request.platform),
            "gis-module": jsonpickle.decode(request.gis_module),
            "cf-module": jsonpickle.decode(request.cf_module)
        }
        result = run_build_model(input_data=input_dict)
        return BuildModelOutput(
            Cost=json.dumps(result["Cost"]),
            AccumulatedNewCapacity=json.dumps(result["AccumulatedNewCapacity"]),
            AccumulatedNewStorageCapacity=json.dumps(result["AccumulatedNewStorageCapacity"]),
            AnnualTechnologyEmission=json.dumps(result["AnnualTechnologyEmission"]),
            ProductionByTechnology=json.dumps(result["ProductionByTechnology"]),
            StorageLevelTimesliceStart=json.dumps(result["StorageLevelTimesliceStart"]),
            TotalEmissions=json.dumps(result["TotalEmissions"]),
            DiscountedCapitalInvestmentByTechnology=json.dumps(result["DiscountedCapitalInvestmentByTechnology"]),
            DiscountedCapitalInvestmentByStorage=json.dumps(result["DiscountedCapitalInvestmentByStorage"]),
            DiscountedSalvageValueByTechnology=json.dumps(result["DiscountedSalvageValueByTechnology"]),
            DiscountedSalvageValueByStorage=json.dumps(result["DiscountedSalvageValueByStorage"]),
            TotalDiscountedFixedOperatingCost=json.dumps(result["TotalDiscountedFixedOperatingCost"]),
            VariableOMCost=json.dumps(result["VariableOMCost"]),
            ex_capacities=json.dumps(result["ex_capacities"]),
            ProductionByTechnologyMM=json.dumps(result["ProductionByTechnologyMM"]),
            report=result["report"],
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_TEOModuleServicer_to_server(TEOModule(), server)

    server.add_insecure_port(f"{os.getenv('GRPC_HOST')}:{os.getenv('GRPC_PORT')}")
    print(f"TEO module Listening at {os.getenv('GRPC_HOST')}:{os.getenv('GRPC_PORT')}")

    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
