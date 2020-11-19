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

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            if node.module is not None:
                key = f'{node.module}.{alias.name}'
                if key not in self._import:
                    if alias.asname is None:
                        if alias.name not in self._import.inverse:
                            self._import[key] = alias.name
                    else:
                        if alias.asname not in self._import.inverse:
                            self._import[key] = alias.asname
        self.generic_visit(node)

    def visit_MatMult(self, node) -> None:
        self.errors.add(
            (node._pyflakes_parent.lineno,
             node._pyflakes_parent.col_offset,
             self.KB['MatMult'][0]['msg']))
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        fqn = attr2str(node)
        for data, rule_name in zip(
                (node.attr, fqn), ('attribute_rules', 'fully_qualified_name_rules')):
            for rule in self.KB[rule_name]:
                msg = rule['msg']
                if data in rule['patterns']:
                    if msg.find('{') > -1:
                        msg = msg.replace('{}', data)
                    self.errors.add((node.lineno, node.col_offset, msg))
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        data = node.id
        rule_name = 'name_only_rules'
        for rule in self.KB[rule_name]:
            msg = rule['msg']
            if data in rule['patterns']:
                if msg.find('{') > -1:
                    msg = msg.replace('{}', data)
                self.errors.add((node.lineno, node.col_offset, msg))
        self.generic_visit(node)


class Flake8TensorsPlugin:
    name = __title__
    version = __version__

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:

        visitor = Visitor()
        visitor.visit(self._tree)

        for line, col, msg in visitor.errors:
            yield line, col, msg, type(self)


RULES = """
attribute_rules:
    - msg: "WT101 {}(): Use rearrange(X, '...->...') from https://github.com/arogozhnikov/einops"
      patterns: ['permute','view','reshape','transpose','flatten','ravel','unravel','squeeze','unsqueeze','chunk','stack', 'concatenate','cat','dstack','hstack','vstack']

    - msg: "WT103 {}(): Use reduce(X, '...->...') from https://github.com/arogozhnikov/einops"
      patterns: ['maximum','minimum','median','average','max_pool3d', 'max_pool2d', 'max_pool1d','avg_pool3d', 'avg_pool2d', 'avg_pool1d']

    - msg: "WT106 {}(): use opt_einsum.contract from https://github.com/dgasmith/opt_einsum"
      patterns: ['einsum','matmul','mm', 'bmm','dot']

    - msg: "WT301 .clone(): use .copy() for numpy-compatible names (Pytorch 1.7+)"
      patterns: ['clone']

    - msg: "WT402 Use focal loss instead of cross entropy loss. See: https://arxiv.org/abs/1708.02002"
      patterns: ['categorical_crossentropy']

name_only_rules:
    - msg: "WT100 {}(): Use Rearrange('...->...') from https://github.com/arogozhnikov/einops"
      patterns: ['PixelShuffle','Concatenate','Flatten','Reshape', 'Stack']

    - msg: "WT102 {}(): Use Reduce('...->...') from https://github.com/arogozhnikov/einops"
      patterns: ['MaxPool3d', 'MaxPool2d', 'MaxPool1d','AvgPool3d', 'AvgPool2d', 'AvgPool1d', 'MaxPool3D', 'MaxPool2D', 'MaxPool1D','AveragePooling1D', 'AveragePooling2D', 'AveragePooling3D','Maximum','Minimum','Average']

    - msg: "WT104 {}(): Use Repeat('...->...') from https://github.com/arogozhnikov/einops"
      patterns: [ ]

    - msg: "WT200 Beware with Pytorch's DropOut2d/DropOut3d! They ALWAYS drop 2nd dimension ONLY."
      patterns: ['DropOut2d','DropOut3d', 'dropout2d','dropout3d']

    - msg: "WT201 Beware: InstanceNorm*d has affine=False as default, unlike in BatchNorm and GroupNorm! See: https://github.com/pytorch/pytorch/issues/22755"
      patterns: ['InstanceNorm1d','InstanceNorm2d','InstanceNorm3d']

    - msg: "WT400 {} layer: consider using butterfly layer. https://github.com/HazyResearch/butterfly"
      patterns: ['Linear','Dense']

    - msg: "WT401 Try AdaBelief optimizer instead of {}. See: https://juntang-zhuang.github.io/adabelief/"
      patterns: ['Adam','SGD']

    - msg: "WT402 Use focal loss instead of cross entropy loss. See: https://arxiv.org/abs/1708.02002"
      patterns: ['CrossEntropyLoss','BinaryCrossEntropy', 'CategoricalCrossEntropy', 'binary_cross_entropy', 'BCELoss', 'categorical_crossentropy']


fully_qualified_name_rules:
    - msg: "WT400 {} layer: consider using butterfly layer. https://github.com/HazyResearch/butterfly"
      patterns: ['nn.Linear','torch.nn.Linear']

    - msg: "WT105 {}(): Use repeat(X, '...->...') from https://github.com/arogozhnikov/einops"
      patterns: ['torch.repeat', 'numpy.repeat','numpy.tile', 'np.tile']

    - msg: "WT108 {}: use bottleneck instead of numpy! Check out: https://github.com/pydata/bottleneck"
      patterns: ["np.nansum", "np.nanmean", "np.nanstd", "np.nanvar", "np.nanmin", "np.nanmax", "np.median", "np.nanmedian", "np.ss", "np.nanargmin", "np.nanargmax", "np.anynan", "np.allnan", "np.rankdata", "np.nanrankdata", "np.partition", "np.argpartition", "np.replace", "np.push", "np.move_sum", "np.move_mean", "np.move_std", "np.move_var", "np.move_min", "np.move_max", "np.move_argmin", "np.move_argmax", "np.move_median", "np.move_rank", "numpy.nansum", "numpy.nanmean", "numpy.nanstd", "numpy.nanvar", "numpy.nanmin", "numpy.nanmax", "numpy.median", "numpy.nanmedian", "numpy.ss", "numpy.nanargmin", "numpy.nanargmax", "numpy.anynan", "numpy.allnan", "numpy.rankdata", "numpy.nanrankdata", "numpy.partition", "numpy.argpartition", "numpy.replace", "numpy.push", "numpy.move_sum", "numpy.move_mean", "numpy.move_std", "numpy.move_var", "numpy.move_min", "numpy.move_max", "numpy.move_argmin", "numpy.move_argmax", "numpy.move_median", "numpy.move_rank" ]

    - msg: "WT300 torch.nn.Module: use nn.Module. Shorter code is more readable."
      patterns: ['torch.nn.Module']



MatMult:
    - msg: "WT107 matrix multiplication (@): use opt_einsum.contract from https://github.com/dgasmith/opt_einsum"
"""
