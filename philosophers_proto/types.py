"""
Data types management for .proto files compilation
"""

import enum


# todo: finish datatype mappings
class DataType(enum.Enum):
    int = 'int'
    float = 'float'
    rpc = 'rpc'
    message = 'message'
    double = 'double'
    int16 = 'int16'
    int32 = 'int32'
    int64 = 'int64'
    long = 'long'
    repeated = 'repeated'
