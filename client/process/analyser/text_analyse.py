#encoding=utf-8
import sys
from poppy import client as poppy
from servers.analyser import analyse_service_pb2 as analyse_service
from servers.analyser import common_pb2 as common

SERVER_CHANNEL = poppy.RpcChannel("127.0.0.1:1314")
SERVER = analyse_service.AnalyseServer_Stub(SERVER_CHANNEL)

def parse(text, enc='utf-8', lang='zh_CN'):
    if isinstance(text, unicode):
        text = text.encode(enc, 'ignore')
    controller = poppy.RpcController()
    # controller.SetTimeout(2000)
    input = common.Input()
    input.raw_text = text
    input.encoding = enc
    input.lang = lang
    output = SERVER.GetResult(controller, input, None)
    if controller.Failed():
        print controller.ErrorText()
        return None
    else:
        return output

if __name__ == "__main__":
    output = parse('刘占亮你好')
    print output
    print output.raw_text
    print type(output.seg_terms)
    for i in output.seg_terms:
        print i.text
    for i in output.entity_terms:
        print i.text
