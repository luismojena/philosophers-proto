"""
This module defines the classes for building the AST for a .proto file
"""

import dataclasses
import abc


@dataclasses.dataclass
class AST(metaclass=abc.ABCMeta):
    name: str = 'AST'

    @abc.abstractmethod
    def build(self):
        return NotImplemented


@dataclasses.dataclass
class ASTSyntax(AST):
    name: str = 'syntax'
    protocol_version: int = 3  # default protocol_version to 3

    def build(self):
        return f"{self.name} = {self.protocol_version};"


@dataclasses.dataclass
class ASTMessage(AST):
    name: str = 'message'

    def build(self):
        return NotImplemented
