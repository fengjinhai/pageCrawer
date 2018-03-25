#!/usr/bin/env python
# -*- coding: cp936 -*-
#

from google.protobuf import message
from google.protobuf import service
import poppy_client
import rpc_error_code_info_pb2
import rpc_option_pb2

RPC_SUCCESS = rpc_error_code_info_pb2.RPC_SUCCESS
RPC_ERROR_PARSE_REQUEST_MESSAGE = rpc_error_code_info_pb2.RPC_ERROR_PARSE_REQUEST_MESSAGE
RPC_ERROR_PARSE_RESPONES_MESSAGE = rpc_error_code_info_pb2.RPC_ERROR_PARSE_RESPONES_MESSAGE
RPC_ERROR_UNCOMPRESS_MESSAGE = rpc_error_code_info_pb2.RPC_ERROR_UNCOMPRESS_MESSAGE
RPC_ERROR_COMPRESS_TYPE = rpc_error_code_info_pb2.RPC_ERROR_COMPRESS_TYPE
RPC_ERROR_NOT_SPECIFY_METHOD_NAME = rpc_error_code_info_pb2.RPC_ERROR_NOT_SPECIFY_METHOD_NAME
RPC_ERROR_METHOD_NAME = rpc_error_code_info_pb2.RPC_ERROR_METHOD_NAME
RPC_ERROR_FOUND_SERVICE = rpc_error_code_info_pb2.RPC_ERROR_FOUND_SERVICE
RPC_ERROR_FOUND_METHOD = rpc_error_code_info_pb2.RPC_ERROR_FOUND_METHOD
RPC_ERROR_CHANNEL_SHUTDOWN = rpc_error_code_info_pb2.RPC_ERROR_CHANNEL_SHUTDOWN
RPC_ERROR_CONNECTION_CLOSED = rpc_error_code_info_pb2.RPC_ERROR_CONNECTION_CLOSED
RPC_ERROR_REQUEST_TIMEOUT = rpc_error_code_info_pb2.RPC_ERROR_REQUEST_TIMEOUT
RPC_ERROR_SERVER_UNAVAILABLE = rpc_error_code_info_pb2.RPC_ERROR_SERVER_UNAVAILABLE
#RPC_ERROR_SERVICE_UNREACHABLE = rpc_error_code_info_pb2.RPC_ERROR_SERVICE_UNREACHALBLE;
RPC_ERROR_SERVER_UNREACHABLE = rpc_error_code_info_pb2.RPC_ERROR_SERVER_UNREACHABLE
RPC_ERROR_NO_AUTH = rpc_error_code_info_pb2.RPC_ERROR_NO_AUTH
RPC_ERROR_NETWORK_UNREACHABLE = rpc_error_code_info_pb2.RPC_ERROR_NETWORK_UNREACHABLE
RPC_ERROR_UNKNOWN = rpc_error_code_info_pb2.RPC_ERROR_UNKNOWN
RPC_ERROR_FROM_USER = rpc_error_code_info_pb2.RPC_ERROR_FROM_USER

CompressTypeNone = rpc_option_pb2.CompressTypeNone
CompressTypeSnappy = rpc_option_pb2.CompressTypeSnappy

RpcClient = poppy_client.RpcClient

rpc_client = RpcClient()

class CachedDict(dict):
    def __init__(self, get_value_function):
        self.get_value_function = get_value_function

    def get(self, key):
        val = super(CachedDict, self).get(key)
        if not val:
            val = self.get_value_function(key)
            super(CachedDict, self).__setitem__(key, val)
        return val

def GetMetaData(method_descriptor):
    if method_descriptor.GetOptions().HasExtension(rpc_option_pb2.method_timeout):
        method_timeout = method_descriptor.GetOptions().Extensions[ \
                rpc_option_pb2.method_timeout]
    else:
        if method_descriptor.containing_service.GetOptions().HasExtension( \
                    rpc_option_pb2.service_timeout):
            method_timeout = method_descriptor.containing_service.GetOptions( \
                    ).Extensions[rpc_option_pb2.service_timeout]
        else:
            method_timeout = 10000
    if method_descriptor.GetOptions().HasExtension( \
            rpc_option_pb2.request_compress_type):
        request_compress_type = method_descriptor.GetOptions( \
                ).Extensions[rpc_option_pb2.request_compress_type]
    else:
        request_compress_type = rpc_option_pb2.CompressTypeNone
    if method_descriptor.GetOptions().HasExtension( \
            rpc_option_pb2.response_compress_type):
        response_compress_type = method_descriptor.GetOptions( \
                ).Extensions[rpc_option_pb2.response_compress_type]
    else:
        response_compress_type = rpc_option_pb2.CompressTypeNone
    return (method_timeout, request_compress_type, response_compress_type)

def ParseResponse(rpc_controller,
            response_class, response_data):
    response = response_class()
    try:
        response.ParseFromString(response_data)
        return response
    except message.DecodeError:
        rpc_controller.inner_controller.SetFailed(RPC_ERROR_PARSE_RESPONES_MESSAGE)
        return None

class ResponseHandler(poppy_client.ResponseHandler):
    def __init__(self, rpc_controller, response_class, done):
        poppy_client.ResponseHandler.__init__(self)
        self.rpc_controller = rpc_controller
        self.response_class = response_class
        self.done = done
        self.__disown__()

    def Run(self, response_data):
        response = ParseResponse(self.rpc_controller,
                self.response_class, response_data)
        self.done(response)

class RpcChannel(service.RpcChannel):
    def __init__(self, server_address):
        self.inner_channel = \
                poppy_client.RpcChannelSwig(rpc_client, server_address)
        self.method_meta_dict = None

    def CallMethod(self, method_descriptor, rpc_controller,
            request, response_class, done):
        if done:
            response_handler = \
                    ResponseHandler(rpc_controller, response_class, done)
        else:
            response_handler = None

        if not self.method_meta_dict:
            self.method_meta_dict = CachedDict(lambda key: GetMetaData(key))

        val = self.method_meta_dict.get(method_descriptor)
        rpc_controller.inner_controller.set_method_full_name(method_descriptor.full_name)
        if rpc_controller.inner_controller.Timeout() <= 0:
            rpc_controller.inner_controller.SetTimeout(val[0])
        if rpc_controller.use_default_request_compress_type:
            rpc_controller.inner_controller.SetRequestCompressType(val[1])
        if rpc_controller.use_default_response_compress_type:
            rpc_controller.inner_controller.SetResponseCompressType(val[2])

        try:
            response_data = self.inner_channel.RawCallMethod(rpc_controller.inner_controller,
                    request.SerializeToString(), response_handler)
            if not done and not rpc_controller.Failed():
                response = ParseResponse(rpc_controller,
                        response_class, response_data)
                return response
        except message.EncodeError:
            print "Failed to serialize the request message"
            sys.exit(1)
        return None

class RpcController(service.RpcController):
    def __init__(self):
        self.inner_controller = poppy_client.RpcControllerSwig()
        self.Reset = self.inner_controller.Reset
        self.Failed = self.inner_controller.Failed
        self.ErrorText = self.inner_controller.ErrorText
        # self.StartCancel = self.inner_controller.StartCancel
        # self.IsCanceled = self.inner_controller.IsCanceled
        # self.NotifyOnCancel = self.inner_controller.NotifyOnCancel
        self.ErrorCode = self.inner_controller.ErrorCode
        self.SetTimeout = self.inner_controller.SetTimeout
        self.use_default_request_compress_type = True
        self.use_default_response_compress_type = True

    def SetRequestCompressType(self, compress_type):
        self.use_default_request_compress_type = False
        self.inner_controller.SetRequestCompressType(compress_type)

    def SetResponseCompressType(self, compress_type):
        self.use_default_response_compress_type = False
        self.inner_controller.SetResponseCompressType(compress_type)

    def SetFailed(self, reason):
        raise NotImplementedError

    def StartCancel(self):
        raise NotImplementedError

    def IsCanceled(self):
        raise NotImplementedError

    def NotifyOnCancel(self, callback):
        raise NotImplementedError

