"""
Classes and objects for building protocol buffer related files, objects and more
"""
from .ast import AST, ASTSyntax, ASTMessage, ASTAttributesList, ASTAttribute
from .types import TypeResolver, DataType


class ProtobufFileBuilder:
    pass


class ASTBuilder:
    def __init__(self, classes: list):
        self.classes: list = classes
        self.last_number_used = 1

    def build(self) -> AST:
        root: AST = AST()

        # first build the sintax
        root.add_element(self._build_syntax())

        # build the classes as messages
        for cls in self.classes:
            message = self._process_model_class(cls)
            root.add_element(message)

        # todo: build the methods as rpc
        # ...

        # return the root
        return root

    def _process_model_class(self, cls):
        attributes: ASTAttributesList = ASTAttributesList()
        model_name: str = self._get_model_name(cls)

        columns = self._get_attributes_from_model(cls)

        for col in columns:
            ast_attribute: ASTAttribute = self._process_column(col)
            attributes.push(ast_attribute)

        message: ASTMessage = ASTMessage(attributes, model_name)
        self.reset_number()
        return message

    def reset_number(self):
        self.last_number_used = 1

    def _process_column(self, col) -> ASTAttribute:
        data_type: DataType = TypeResolver.from_sqlalchemy(col.type.__class__)
        name: str = col.name
        attribute_number: int = self.get_new_number()
        return ASTAttribute(data_type, name, attribute_number)

    def _get_attributes_from_model(self, cls):
        return cls.__table__.columns.values()

    def _get_model_name(self, cls):
        return cls.__name__

    def _build_syntax(self) -> ASTSyntax:
        return ASTSyntax(3)

    def get_new_number(self) -> int:
        n = self.last_number_used
        self.last_number_used += 1
        return n
