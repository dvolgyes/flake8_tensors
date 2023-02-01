from flake8_tensors import __version__, __title__
from typing import Any
from typing import Generator
from typing import Tuple
from typing import Type
import ast
from ruamel.yaml import YAML
import astpath
from .rules import rules_yaml


class Flake8TensorsPlugin:

    name = __title__
    version = __version__

    def __init__(self, tree: ast.AST):
        self._tree = tree
        self.rules = YAML(typ='safe').load(rules_yaml)

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:

        xml = astpath.convert_to_xml(self._tree)

        for rule in self.rules['astpath_rules']:
            msg = rule['msg']
            patterns = rule['patterns']
            template = rule.get('template', [])

            if len(template) > 0:
                for t in template:
                    patterns_ = [p.replace('{}', t) for p in patterns]  # noqa:P103,E501
                    m = msg.replace('{}', t)  # noqa:P103
                    for pattern in patterns_:
                        for line_no in astpath.find_in_ast(xml, pattern):
                            yield line_no, 0, m, type(self)

            else:
                for pattern in patterns:
                    for line_no in astpath.find_in_ast(xml, pattern):
                        yield line_no, 0, msg, type(self)
