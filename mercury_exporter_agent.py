#encoding: utf-8

import requests
import prometheus_client
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask, request, current_app
import os
import sys


Mercury_RPC = sys.argv[1]

NodeFlask = Flask(__name__)

def convert_int(value):
    try:
        return int(value)
    except ValueError:
        return int(value, base=16)
    except Exception as exp:
        raise exp

class RpcGet(object):
    def __init__(self, Mercury_RPC):
        self.Mercury_RPC = Mercury_RPC

    def get_mercury_info(self):
        headers = {"Content-Type":"application/json"}
        data = '{"id":2, "jsonrpc":"2.0", "method":"get_tip", "params":[]}'
        try:
            r = requests.post(
                url="%s" %(self.Mercury_RPC),
                data=data,
                headers=headers
            )
            replay = r.json()["result"]
            return {
                "last_blocknumber": convert_int(replay["block_number"]),
                "last_block_hash": str(replay["block_hash"]),
            }
        except:
            return {
                "last_blocknumber": "-1",
                "last_block_hash": "-1",
            }

@NodeFlask.route("/metrics/mercury")
def rpc_get():
    CKB_Chain = CollectorRegistry(auto_describe=False)
    Get_Mercury_Info = Gauge("Get_Mercury_LastBlockInfo",
                                   "Get LastBlockInfo, Show Mercury latest block height",
                                   ["mercury_rpc"],
                                   registry=CKB_Chain)

    get_result = RpcGet(Mercury_RPC)
    mercury_last_block_info = get_result.get_mercury_info()
    Get_Mercury_Info.labels(
        mercury_rpc=Mercury_RPC
    ).set(mercury_last_block_info["last_blocknumber"])
    return Response(prometheus_client.generate_latest(CKB_Chain), mimetype="text/plain")

if __name__ == "__main__":
    NodeFlask.run(host="0.0.0.0",port=3000)
