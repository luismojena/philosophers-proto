"""
Classes for building the AST for a .proto file
"""

import dataclasses
import abc
from queue import PriorityQueue, Empty
import typing
from .types import DataType


class AST(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def build(self) -> str:
        return NotImplemented


@dataclasses.dataclass
class ASTSyntax(AST):
    command: str = dataclasses.field(default='syntax', init=False)
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
        # FIXME: check protocol specification for numbers that can't be used
        self.proto_dgram_number = value

    def build(self) -> str:
        return f"{self.data_type} {self.name} = {self.protocol_datagram_number};"


@dataclasses.dataclass
class ASTAttributesList(AST):
    _queue: PriorityQueue = PriorityQueue()

    def pop(self) -> typing.Union[None, ASTAttribute]:
        try:
            el = self._queue.get(False)
        except Empty:
            return None
        else:
            return el

    def pop_str(self) -> str:
        el = self.pop()
        return '' if el is None else el.build()

    def build(self) -> str:
        return_str: str = ''
        while not self._queue.empty():
            ast_attibute: str = self.pop_str()
            return_str += f"{ast_attibute}\n"
        return return_str


@dataclasses.dataclass
class ASTMessage(AST):
    command: str = dataclasses.field(default='message', init=False)
    attributes_list: ASTAttributesList = dataclasses.field(repr=False)
    name: str = ''

    def build(self) -> str:
        return f"""
        message {self.name} {{
            {self.attributes_list.build()}
        }}
        """
