# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


DESCRIPTOR = descriptor.FileDescriptor(
  name='common.proto',
  package='tencent.search.isoso',
  serialized_pb='\n\x0c\x63ommon.proto\x12\x14tencent.search.isoso\"G\n\x05Input\x12\x10\n\x08raw_text\x18\x01 \x02(\x0c\x12\x17\n\x08\x65ncoding\x18\x02 \x02(\x0c:\x05utf-8\x12\x13\n\x04lang\x18\x03 \x02(\x0c:\x05zh_CN\"N\n\x0eNormalizedText\x12\x0c\n\x04text\x18\x01 \x02(\x0c\x12\x0c\n\x04type\x18\x02 \x02(\x05\x12\x0e\n\x06weight\x18\x03 \x01(\x02\x12\x10\n\x08type_str\x18\x04 \x01(\x0c\"3\n\x07SynText\x12\x0c\n\x04text\x18\x01 \x02(\x0c\x12\x0c\n\x04\x63onf\x18\x02 \x02(\x02\x12\x0c\n\x04type\x18\x03 \x02(\x05\"P\n\x07SegTerm\x12\x0c\n\x04text\x18\x01 \x02(\x0c\x12\r\n\x05start\x18\x02 \x02(\x05\x12\x0b\n\x03\x65nd\x18\x03 \x02(\x05\x12\x0b\n\x03pos\x18\x04 \x01(\x05\x12\x0e\n\x06weight\x18\x05 \x01(\x02\"\xa5\x01\n\nEntityTerm\x12\x0c\n\x04text\x18\x01 \x02(\x0c\x12\r\n\x05start\x18\x02 \x02(\x05\x12\x0b\n\x03\x65nd\x18\x03 \x02(\x05\x12\x0c\n\x04type\x18\x04 \x02(\x05\x12\x38\n\nnorm_texts\x18\x05 \x03(\x0b\x32$.tencent.search.isoso.NormalizedText\x12\x10\n\x08type_str\x18\x06 \x01(\x0c\x12\x13\n\x0b\x66ind_source\x18\x07 \x01(\x0c\"o\n\x07SynTerm\x12\x0c\n\x04text\x18\x01 \x02(\x0c\x12\x12\n\nterm_start\x18\x02 \x02(\x05\x12\x10\n\x08term_end\x18\x03 \x02(\x05\x12\x30\n\tsyn_texts\x18\x04 \x03(\x0b\x32\x1d.tencent.search.isoso.SynText\"\xca\x01\n\x06Output\x12\x10\n\x08raw_text\x18\x01 \x02(\x0c\x12\x30\n\tseg_terms\x18\x02 \x03(\x0b\x32\x1d.tencent.search.isoso.SegTerm\x12\x36\n\x0c\x65ntity_terms\x18\x03 \x03(\x0b\x32 .tencent.search.isoso.EntityTerm\x12\x30\n\tsyn_terms\x18\x04 \x03(\x0b\x32\x1d.tencent.search.isoso.SynTerm\x12\x12\n\ndebug_info\x18\x05 \x03(\x0c\"T\n\nEntityItem\x12\x0c\n\x04type\x18\x01 \x02(\x05\x12\x38\n\nnorm_texts\x18\x02 \x03(\x0b\x32$.tencent.search.isoso.NormalizedText\"C\n\tLabelItem\x12\x36\n\x0c\x65ntity_items\x18\x01 \x03(\x0b\x32 .tencent.search.isoso.EntityItem')




_INPUT = descriptor.Descriptor(
  name='Input',
  full_name='tencent.search.isoso.Input',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='raw_text', full_name='tencent.search.isoso.Input.raw_text', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='encoding', full_name='tencent.search.isoso.Input.encoding', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=True, default_value="utf-8",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='lang', full_name='tencent.search.isoso.Input.lang', index=2,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=True, default_value="zh_CN",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=38,
  serialized_end=109,
)


_NORMALIZEDTEXT = descriptor.Descriptor(
  name='NormalizedText',
  full_name='tencent.search.isoso.NormalizedText',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='text', full_name='tencent.search.isoso.NormalizedText.text', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='type', full_name='tencent.search.isoso.NormalizedText.type', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='weight', full_name='tencent.search.isoso.NormalizedText.weight', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='type_str', full_name='tencent.search.isoso.NormalizedText.type_str', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=111,
  serialized_end=189,
)


_SYNTEXT = descriptor.Descriptor(
  name='SynText',
  full_name='tencent.search.isoso.SynText',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='text', full_name='tencent.search.isoso.SynText.text', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='conf', full_name='tencent.search.isoso.SynText.conf', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='type', full_name='tencent.search.isoso.SynText.type', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=191,
  serialized_end=242,
)


_SEGTERM = descriptor.Descriptor(
  name='SegTerm',
  full_name='tencent.search.isoso.SegTerm',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='text', full_name='tencent.search.isoso.SegTerm.text', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='start', full_name='tencent.search.isoso.SegTerm.start', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='end', full_name='tencent.search.isoso.SegTerm.end', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='pos', full_name='tencent.search.isoso.SegTerm.pos', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='weight', full_name='tencent.search.isoso.SegTerm.weight', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=244,
  serialized_end=324,
)


_ENTITYTERM = descriptor.Descriptor(
  name='EntityTerm',
  full_name='tencent.search.isoso.EntityTerm',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='text', full_name='tencent.search.isoso.EntityTerm.text', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='start', full_name='tencent.search.isoso.EntityTerm.start', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='end', full_name='tencent.search.isoso.EntityTerm.end', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='type', full_name='tencent.search.isoso.EntityTerm.type', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='norm_texts', full_name='tencent.search.isoso.EntityTerm.norm_texts', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='type_str', full_name='tencent.search.isoso.EntityTerm.type_str', index=5,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='find_source', full_name='tencent.search.isoso.EntityTerm.find_source', index=6,
      number=7, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=327,
  serialized_end=492,
)


_SYNTERM = descriptor.Descriptor(
  name='SynTerm',
  full_name='tencent.search.isoso.SynTerm',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='text', full_name='tencent.search.isoso.SynTerm.text', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='term_start', full_name='tencent.search.isoso.SynTerm.term_start', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='term_end', full_name='tencent.search.isoso.SynTerm.term_end', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='syn_texts', full_name='tencent.search.isoso.SynTerm.syn_texts', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=494,
  serialized_end=605,
)


_OUTPUT = descriptor.Descriptor(
  name='Output',
  full_name='tencent.search.isoso.Output',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='raw_text', full_name='tencent.search.isoso.Output.raw_text', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='seg_terms', full_name='tencent.search.isoso.Output.seg_terms', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='entity_terms', full_name='tencent.search.isoso.Output.entity_terms', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='syn_terms', full_name='tencent.search.isoso.Output.syn_terms', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='debug_info', full_name='tencent.search.isoso.Output.debug_info', index=4,
      number=5, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=608,
  serialized_end=810,
)


_ENTITYITEM = descriptor.Descriptor(
  name='EntityItem',
  full_name='tencent.search.isoso.EntityItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='type', full_name='tencent.search.isoso.EntityItem.type', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='norm_texts', full_name='tencent.search.isoso.EntityItem.norm_texts', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=812,
  serialized_end=896,
)


_LABELITEM = descriptor.Descriptor(
  name='LabelItem',
  full_name='tencent.search.isoso.LabelItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='entity_items', full_name='tencent.search.isoso.LabelItem.entity_items', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=898,
  serialized_end=965,
)


_ENTITYTERM.fields_by_name['norm_texts'].message_type = _NORMALIZEDTEXT
_SYNTERM.fields_by_name['syn_texts'].message_type = _SYNTEXT
_OUTPUT.fields_by_name['seg_terms'].message_type = _SEGTERM
_OUTPUT.fields_by_name['entity_terms'].message_type = _ENTITYTERM
_OUTPUT.fields_by_name['syn_terms'].message_type = _SYNTERM
_ENTITYITEM.fields_by_name['norm_texts'].message_type = _NORMALIZEDTEXT
_LABELITEM.fields_by_name['entity_items'].message_type = _ENTITYITEM

class Input(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _INPUT
  
  # @@protoc_insertion_point(class_scope:tencent.search.isoso.Input)

class NormalizedText(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _NORMALIZEDTEXT
  
  # @@protoc_insertion_point(class_scope:tencent.search.isoso.NormalizedText)

class SynText(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SYNTEXT
  
  # @@protoc_insertion_point(class_scope:tencent.search.isoso.SynText)

class SegTerm(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SEGTERM
  
  # @@protoc_insertion_point(class_scope:tencent.search.isoso.SegTerm)

class EntityTerm(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ENTITYTERM
  
  # @@protoc_insertion_point(class_scope:tencent.search.isoso.EntityTerm)

class SynTerm(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SYNTERM
  
  # @@protoc_insertion_point(class_scope:tencent.search.isoso.SynTerm)

class Output(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _OUTPUT
  
  # @@protoc_insertion_point(class_scope:tencent.search.isoso.Output)

class EntityItem(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ENTITYITEM
  
  # @@protoc_insertion_point(class_scope:tencent.search.isoso.EntityItem)

class LabelItem(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LABELITEM
  
  # @@protoc_insertion_point(class_scope:tencent.search.isoso.LabelItem)

# @@protoc_insertion_point(module_scope)
