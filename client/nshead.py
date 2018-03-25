# -*- coding:utf-8 -*
import struct

from ctypes import *

# NSHEAD_MAGICNUM = 0xfb709394;                                                                                                                                                         

class NsHead(Structure):
    _fields_ = [
        ('id', c_uint16),
        ('version', c_uint16),
        ('log_id', c_uint32),
        ('provider', c_char * 16),
        ('magic_num', c_uint32),
        ('reserved', c_uint32),
        ('body_len', c_uint32),
        ]
    
    def __init__(self):
		self.id = 0
		self.magic_num = 0xfb709394
		self.log_id = 0
		self.provider = ''
		self.reserverd = 0

    def pack(self):
        return struct.pack("HHI16sIII", self.id, self.version, self.log_id, self.provider, self.magic_num, self.reserved, self.body_len)

    to_str = pack

    @classmethod
    def from_str(cls, string):
		"""
		长度校验
		"""
		if len(string) != sizeof(cls):
			return False
		buf = create_string_buffer(string)
		return cls.from_buffer(buf)

    def __str__(self):
        return "<NsHead id:%d logid:%d provider:%s magic:0x%X bodylen:%s>" % (
            self.id, self.log_id, self.provider, self.magic_num, self.body_len)
