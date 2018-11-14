"""
Classes for building the AST for a .proto file
"""

import dataclasses
import abc
from queue import PriorityQueue, Empty
import typing
from .types import DataType

# fixme: convert this into a configurable option
DEFAULT_INDENTATION_SPACES = 4
DEFAULT_INDENTATION = DEFAULT_INDENTATION_SPACES * ' '


class AbstractAST(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def build(self) -> str:
        return NotImplemented


@dataclasses.dataclass
class AST(AbstractAST):
    elements: typing.List[AbstractAST] = dataclasses.field(default_factory=list)

    def build(self) -> str:
        return ''.join([i.build() for i in self.elements])

    def add_element(self, ast_element: AbstractAST):
        self.elements.append(ast_element)


@dataclasses.dataclass
class ASTSyntax(AbstractAST):
    command: str = dataclasses.field(default='syntax', init=False)
    protocol_version: int = 3  # default protocol_version to 3

    def build(self) -> str:
        return f"{self.command} = {self.protocol_version};"


@dataclasses.dataclass(order=True)
class ASTAttribute(AbstractAST):
    data_type: DataType = dataclasses.field(compare=False, default=None)
    name: str = dataclasses.field(compare=False, default='')
    proto_dgram_number: int = 0

    @property
    def protocol_datagram_number(self) -> int:
        return self.proto_dgram_number

    @protocol_datagram_number.setter
    def protocol_datagram_number(self, value: int) -> None:
        # FIXME: check protocol specification for numbers that can't be used
        self.proto_dgram_number = value

    def build(self) -> str:
        return f"{DEFAULT_INDENTATION}{self.data_type.name} {self.name} = {self.protocol_datagram_number};"


@dataclasses.dataclass
class ASTAttributesList(AbstractAST):
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

    def push(self, ast_attribute: ASTAttribute):
        self._queue.put(ast_attribute, True)

    def build(self) -> str:
        return_str: str = ''
        while not self._queue.empty():
            ast_attibute: str = self.pop_str()
            return_str += f"{ast_attibute}\n"
        return return_str


@dataclasses.dataclass
class ASTMessage(AbstractAST):
    command: str = dataclasses.field(default='message', init=False)
    attributes_list: ASTAttributesList = dataclasses.field(repr=False)
    name: str = ''

    def build(self) -> str:
        return f"""
message {self.name} {{
{self.attributes_list.build()}
}}
        """
