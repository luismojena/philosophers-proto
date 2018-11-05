"""
This module defines the classes for building the AST for a .proto file
"""

import dataclasses
import abc


@dataclasses.dataclass
class AST(metaclass=abc.ABCMeta):
    command: str = dataclasses.field(default='', repr=False, init=False)

    @abc.abstractmethod
    def build(self):
        return NotImplemented


@dataclasses.dataclass
class ASTSyntax(AST):
    command: str = dataclasses.field(default='syntax', repr=False, init=False)
    protocol_version: int = 3  # default protocol_version to 3

    def build(self):
        return f"{self.command} = {self.protocol_version};"


@dataclasses.dataclass
class ASTMessage(AST):
    command: str = dataclasses.field(default='message', repr=False, init=False)
    name: str = ''

    def build(self):
        return NotImplemented
