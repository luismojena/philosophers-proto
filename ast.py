"""
Classes for building the AST for a .proto file
"""

import dataclasses
import abc
import typing
from .types import DataType


@dataclasses.dataclass
class AST(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def build(self) -> str:
        return NotImplemented


@dataclasses.dataclass
class ASTSyntax(AST):
    command: str = dataclasses.field(default='syntax', repr=False, init=False)
    protocol_version: int = 3  # default protocol_version to 3

    def build(self) -> str:
        return f"{self.command} = {self.protocol_version};"


@dataclasses.dataclass
class ASTAttribute(AST):
    data_type: DataType = None
    name: str = ''
    proto_dgram_number: int = 0

    @property
    def protocol_datagram_number(self) -> int:
        return self.proto_dgram_number

    @protocol_datagram_number.setter
    def protocol_datagram_number(self, value: int) -> None:
        # FIXME: check protocol specification for numbers that cant be used
        self.proto_dgram_number = value

    def build(self) -> str:
        return f"{self.data_type} {self.name} = {self.protocol_datagram_number};"


@dataclasses.dataclass
class ASTAttributesList(AST, list):

    def build(self) -> str:
        return NotImplemented


@dataclasses.dataclass
class ASTMessage(AST):
    command: str = dataclasses.field(default='message', repr=False, init=False)
    name: str = ''
    attributes_list: ASTAttributesList = dataclasses.field(default_factory=list, repr=False)

    def build(self) -> str:
        return NotImplemented
