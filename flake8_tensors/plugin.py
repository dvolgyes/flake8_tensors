from flake8_tensors import __version__, __title__
import ast
from typing import Any
from typing import Dict
from typing import Generator
from typing import List
from typing import Tuple
from typing import Type
from typing import Set
import bidict
import yaml
import astpath


def attr2str(node):
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return attr2str(node.value) + '.' + attr2str(node.attr)
    elif isinstance(node, str):
        return node
    elif isinstance(node, ast.Constant):
        return repr(node.value)
    elif isinstance(node, ast.Call):
        x = f"{attr2str(node.func)}({', '.join([attr2str(x) for x in node.args])},{', '.join(attr2str(x) for x in node.keywords)})"
        return x
    return ""  # empty for not implemented


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: Set[Tuple[int, int, str]] = set()
        self._from_imports: Dict[str, str] = {}
        self.KB = yaml.safe_load(RULES)
        self._import = bidict.bidict()

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            fullname = alias.name
            while (basename := fullname.split('.')[0]) in self._import.inv:
                new_basename = self._import.inv[basename]
                fullname = '.'.join([new_basename, ] + fullname.split('.')[1:])
                if basename == new_basename:
                    break
            try:
                if alias.asname is not None:
                    self._import[fullname] = alias.asname
                else:
                    self._import[fullname] = alias.name
            except bidict.ValueDuplicationError:
                pass  #  There might be some false positives, but unlikely
        self.generic_visit(node)

    # ~ def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        # ~ for alias in node.names:
            # ~ if node.module is not None:
                # ~ key = f'{node.module}.{alias.name}'
                # ~ if key not in self._import:
                    # ~ if alias.asname is None:
                        # ~ if alias.name not in self._import.inverse:
                            # ~ self._import[key] = alias.name
                    # ~ else:
                        # ~ if alias.asname not in self._import.inverse:
                            # ~ self._import[key] = alias.asname
        # ~ self.generic_visit(node)


    def visit_Attribute(self, node: ast.Attribute) -> None:
        fqn = attr2str(node)
        for data, rule_name in zip((fqn,), ('fully_qualified_name_rules',)):
            for rule in self.KB[rule_name]:
                msg = rule['msg']
                if data in rule['patterns']:
                    if msg.find('{') > -1:
                        msg = msg.replace('{}', data)
                    self.errors.add((node.lineno, node.col_offset, msg))
        self.generic_visit(node)

    # ~ def visit_Name(self, node: ast.Name) -> None:
        # ~ data = node.id
        # ~ rule_name = 'name_only_rules'
        # ~ for rule in self.KB[rule_name]:
            # ~ msg = rule['msg']
            # ~ if data in rule['patterns']:
                # ~ if msg.find('{') > -1:
                    # ~ msg = msg.replace('{}', data)
                # ~ self.errors.add((node.lineno, node.col_offset, msg))
        # ~ self.generic_visit(node)


class Flake8TensorsPlugin:
    name = __title__
    version = __version__

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:

        xml = astpath.convert_to_xml(self._tree)

        rules = yaml.safe_load(RULES)
        for rule in rules['astpath_rules']:
            msg = rule['msg']
            patterns = rule['patterns']
            template = rule.get('template',[])

            if len(template) > 0:
                for t in template:
                    patterns_ = [p.replace('{}',t) for p in patterns]
                    m = msg.replace('{}',t)
                    for pattern in patterns_:
                        for l in astpath.find_in_ast(xml,pattern):
                            yield l, 0, m, type(self)

            else:
                for pattern in patterns:
                    for l in astpath.find_in_ast(xml,pattern):
                        yield l, 0, msg, type(self)
        return
        visitor = Visitor()
        visitor.visit(self._tree)

        for line, col, msg in visitor.errors:
            yield line, col, msg, type(self)


RULES = """
astpath_rules:
    - msg: "WT100 {}(): Use Rearrange('...->...') from https://github.com/arogozhnikov/einops"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['PixelShuffle','Concatenate','Flatten','Reshape', 'Stack']

    - msg: "WT101 X.{}(): Use rearrange(X, '...->...') from https://github.com/arogozhnikov/einops"
      patterns: [".//Call/func/Attribute[@attr='{}' and ancestor::Call]", ]
      template: ['permute','view','reshape','transpose','flatten','ravel','unravel','squeeze','unsqueeze','chunk','stack', 'concatenate','cat','dstack','hstack','vstack']

    - msg: "WT102 {}(): Use Reduce('...->...') from https://github.com/arogozhnikov/einops"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['MaxPool3d', 'MaxPool2d', 'MaxPool1d','AvgPool3d', 'AvgPool2d', 'AvgPool1d', 'MaxPool3D', 'MaxPool2D', 'MaxPool1D','AveragePooling1D', 'AveragePooling2D', 'AveragePooling3D','Maximum','Minimum','Average']

    - msg: "WT103 {}(): Use reduce(X, '...->...') from https://github.com/arogozhnikov/einops"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['maximum','minimum','median','average','max_pool3d', 'max_pool2d', 'max_pool1d','avg_pool3d', 'avg_pool2d', 'avg_pool1d']

    - msg: "WT102 {}(): Use Repeat('...->...') from https://github.com/arogozhnikov/einops"
      patterns: [ ]
      template: [ ]

    - msg: "WT105 np.{}(): Use repeat(X, '...->...') from https://github.com/arogozhnikov/einops"
      patterns: [".//Call/func/Attribute[(value/Name/@id='np' or value/Name/@id='numpy') and @attr='{}']", ]
      template: ['tile', 'repeat']

    - msg: "WT105 torch.repeat(): Use repeat(X, '...->...') from https://github.com/arogozhnikov/einops"
      patterns: [".//Call/func/Attribute[value/Name/@id='torch' and @attr='repeat']", ]

    - msg: "WT106 {}(): use opt_einsum.contract from https://github.com/dgasmith/opt_einsum"
      patterns: [".//Call/func/Attribute[@attr='{}']",]
      template: ['einsum','matmul','mm', 'bmm','dot']

    - msg: "WT107 matrix multiplication (@): use opt_einsum.contract from https://github.com/dgasmith/opt_einsum"
      patterns: [".//MatMult",]


    - msg: "WT200 Beware with Pytorch's DropOut2d/DropOut3d! They ALWAYS drop 2nd dimension ONLY."
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['DropOut2d','DropOut3d', 'dropout2d','dropout3d']

    - msg: "WT201 Beware: InstanceNorm*d has affine=False as default, unlike in BatchNorm and GroupNorm! See: https://github.com/pytorch/pytorch/issues/22755"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['InstanceNorm1d','InstanceNorm2d','InstanceNorm3d']


    - msg: "WT300 torch.nn.X: use nn.X. Shorter code is more readable."
      patterns: ["//Name[@id='torch' and ../../../Attribute/@attr='nn' and not(ancestor::Import or ancestor::ImportFrom)]",]
      template: [ ]

    - msg: "WT301 .clone(): use .copy() for numpy-compatible names (Pytorch 1.7+)"
      patterns: [".//Call/func/Attribute[@attr='clone']",]
      template: ['clone']


    - msg: "WT402 Use focal loss instead of cross entropy loss. See: https://arxiv.org/abs/1708.02002"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['categorical_crossentropy']

    - msg: "WT400 {} layer: consider using butterfly layer. https://github.com/HazyResearch/butterfly"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['Linear','Dense']

    - msg: "WT401 Try AdaBelief optimizer instead of {}. See: https://juntang-zhuang.github.io/adabelief/"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['Adam','SGD']

    - msg: "WT402 Use focal loss instead of cross entropy loss. See: https://arxiv.org/abs/1708.02002"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['CrossEntropyLoss','BinaryCrossEntropy', 'CategoricalCrossEntropy', 'binary_cross_entropy', 'BCELoss', 'categorical_crossentropy']

    - msg: "WT108 np.{}: use bottleneck instead of numpy! Check out: https://github.com/pydata/bottleneck"
      patterns: [".//Call/func/Attribute[(value/Name/@id='np' or value/Name/@id='numpy') and @attr='{}']", ]
      template: ["nansum", "nanmean", "nanstd", "nanvar", "nanmin", "nanmax", "median", "nanmedian", "ss", "nanargmin", "nanargmax", "anynan", "allnan", "rankdata", "nanrankdata", "partition", "argpartition", "replace", "push", "move_sum", "move_mean", "move_std", "move_var", "move_min", "move_max", "move_argmin", "move_argmax", "move_median", "move_rank", "numpy.nansum", "numpy.nanmean", "numpy.nanstd", "numpy.nanvar", "numpy.nanmin", "numpy.nanmax", "numpy.median", "numpy.nanmedian", "numpy.ss", "numpy.nanargmin", "numpy.nanargmax", "numpy.anynan", "numpy.allnan", "numpy.rankdata", "numpy.nanrankdata", "numpy.partition", "numpy.argpartition", "numpy.replace", "numpy.push", "numpy.move_sum", "numpy.move_mean", "numpy.move_std", "numpy.move_var", "numpy.move_min", "numpy.move_max", "numpy.move_argmin", "numpy.move_argmax", "numpy.move_median", "numpy.move_rank" ]


    - msg: "WT108 np.{}: use bottleneck instead of numpy! Check out: https://github.com/pydata/bottleneck"
      patterns: [".//Cons/func/Attribute[(value/Name/@id='np' or value/Name/@id='numpy') and @attr='{}']", ]
      template: ["nansum", "nanmean", "nanstd", "nanvar", "nanmin", "nanmax", "median", "nanmedian", "ss", "nanargmin", "nanargmax", "anynan", "allnan", "rankdata", "nanrankdata", "partition", "argpartition", "replace", "push", "move_sum", "move_mean", "move_std", "move_var", "move_min", "move_max", "move_argmin", "move_argmax", "move_median", "move_rank", "numpy.nansum", "numpy.nanmean", "numpy.nanstd", "numpy.nanvar", "numpy.nanmin", "numpy.nanmax", "numpy.median", "numpy.nanmedian", "numpy.ss", "numpy.nanargmin", "numpy.nanargmax", "numpy.anynan", "numpy.allnan", "numpy.rankdata", "numpy.nanrankdata", "numpy.partition", "numpy.argpartition", "numpy.replace", "numpy.push", "numpy.move_sum", "numpy.move_mean", "numpy.move_std", "numpy.move_var", "numpy.move_min", "numpy.move_max", "numpy.move_argmin", "numpy.move_argmax", "numpy.move_median", "numpy.move_rank" ]


"""
