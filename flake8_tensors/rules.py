rules_yaml = """
astpath_rules:
    - msg: "WT100: (style) {}. Use Rearrange('...->...') from https://github.com/arogozhnikov/einops"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['PixelShuffle','Concatenate','Flatten','Reshape', 'Stack']

    - msg: "WT101: (style) {}.  Use rearrange(X, '...->...') from https://github.com/arogozhnikov/einops"
      patterns: [".//Call/func/Attribute[@attr='{}' and ancestor::Call]", ]
      template: ['moveaxis', 'expand_dims', 'permute','view','reshape','transpose','flatten','ravel','unravel','squeeze','unsqueeze','chunk','stack', 'concatenate','cat','dstack','hstack','vstack']

    - msg: "WT102: (style) {}.  Use Reduce('...->...') from https://github.com/arogozhnikov/einops"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['MaxPool3d', 'MaxPool2d', 'MaxPool1d','AvgPool3d', 'AvgPool2d', 'AvgPool1d', 'MaxPool3D', 'MaxPool2D', 'MaxPool1D','AveragePooling1D', 'AveragePooling2D', 'AveragePooling3D','Maximum','Minimum','Average']

    - msg: "WT103: (style) {}. Use reduce(X, '...->...') from https://github.com/arogozhnikov/einops"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['maximum','minimum','median','average','max_pool3d', 'max_pool2d', 'max_pool1d','avg_pool3d', 'avg_pool2d', 'avg_pool1d']

    - msg: "WT104: (style) {}.  Use Repeat('...->...') from https://github.com/arogozhnikov/einops"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['Repeat']

    - msg: "WT105: (style) np.{}(): Use repeat(X, '...->...') from https://github.com/arogozhnikov/einops"
      patterns: [".//Call/func/Attribute[(value/Name/@id='np' or value/Name/@id='numpy') and @attr='{}']", ]
      template: ['tile', 'repeat']

    - msg: "WT106: (style): use opt_einsum.contract from https://github.com/dgasmith/opt_einsum"
      patterns: [".//Call/func/Attribute[@attr='{}']",]
      template: ['einsum','matmul','mm', 'bmm','dot']

    - msg: "WT107: (style): matrix multiplication (@): use opt_einsum.contract from https://github.com/dgasmith/opt_einsum"
      patterns: [".//MatMult",]

    - msg: "WT108:  (style) np.{}(). Use bottleneck instead of numpy! Check out: https://github.com/pydata/bottleneck"
      patterns: [".//Call/func/Attribute[(value/Name/@id='np' or value/Name/@id='numpy') and @attr='{}']", ]
      template: ["nansum", "nanmean", "nanstd", "nanvar", "nanmin", "nanmax", "median", "nanmedian", "ss", "nanargmin", "nanargmax", "anynan", "allnan", "rankdata", "nanrankdata", "partition", "argpartition", "replace", "push", "move_sum", "move_mean", "move_std", "move_var", "move_min", "move_max", "move_argmin", "move_argmax", "move_median", "move_rank"]

    - msg: "WT109: (style) np.any(np.isnan(x)). Use bn.anynan(x) from bottleneck, it is much faster! https://github.com/pydata/bottleneck"
      patterns: [".//Call[((func/Attribute/value/Name/@id='np' or func/Attribute/value/Name/@id='numpy') and func/Attribute/@attr='any') and args/Call/func/Attribute[(value/Name/@id='np' or value/Name/@id='numpy') and @attr='isnan']]", ]
      template: []

    - msg: "WT110: (style) np.all(np.isnan(x)): use bn.allnan(x) from bottleneck, it is much faster! https://github.com/pydata/bottleneck"
      patterns: [".//Call[((func/Attribute/value/Name/@id='np' or func/Attribute/value/Name/@id='numpy') and func/Attribute/@attr='all') and args/Call/func/Attribute[(value/Name/@id='np' or value/Name/@id='numpy') and @attr='isnan']]", ]
      template: []

    - msg: "WT111: (style) np.{} do you really need an isnan? Can't you use nansum/nanmean/nan* functions? Check out: https://github.com/pydata/bottleneck"
      patterns: [".//Call/func/Attribute[(value/Name/@id='np' or value/Name/@id='numpy') and @attr='{}' and not(ancestor::Call/func/Attribute[(value/Name/@id='np' or value/Name/@id='numpy') and (@attr='any' or @attr='all')]) ]", ]
      template: ["isnan"]

    - msg: "WT113: (style) torch.repeat(): Use repeat(X, '...->...') from https://github.com/arogozhnikov/einops"
      patterns: [".//Call/func/Attribute[value/Name/@id='torch' and @attr='repeat']", ]

    - msg: "WT114: (style) torch.nn.X: use nn.X. Shorter code is more readable."
      patterns: [".//Name[@id='torch' and ../../../Attribute/@attr='nn' and not(ancestor::Import or ancestor::ImportFrom)]",]
      template: [ ]

    - msg: "WT115: (style) .clone(): use .copy() for numpy-compatible names (Pytorch 1.7+)"
      patterns: [".//Call/func/Attribute[@attr='clone']",]
      template: ['clone']


    - msg: "WT200: (warning)  Careful with Pytorch's DropOut2d/DropOut3d! They ALWAYS drop 2nd dimension ONLY."
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['DropOut2d','DropOut3d', 'dropout2d','dropout3d']

    - msg: "WT201: (warning) {} has affine=False as default, unlike in BatchNorm and GroupNorm! Set 'affine' explicitly. See: https://github.com/pytorch/pytorch/issues/22755"
      patterns: [".//Name[@id='{}' and ancestor::Call and not(../../keywords//@arg='affine')]", ".//Attribute[@attr='{}' and ancestor::Call and not(../../keywords//@arg='affine')]"]
      template: ['InstanceNorm1d','InstanceNorm2d','InstanceNorm3d']

    - msg: "WT203: (warning) .{}() calls also need to assign to a new variable, they do NOT change their underlying variable"
      patterns: [".//Expr/value/Call/func/Attribute[@attr='{}']", ]
      template: ['cpu', 'detach', 'permute','view','reshape','transpose','flatten','ravel','unravel','squeeze','unsqueeze','chunk','stack', 'concatenate','cat','dstack','hstack','vstack']



    - msg: "WT302: (performance) astype() always makes a copy!!! use explicit .astype(..., copy=True/False)"
      patterns: [".//Call[func/Attribute[@attr='astype'] and not(keywords/keyword[@arg='copy'])]"]

    - msg: 'WT303: (performance) astype({}) is not precise enough (default is 64bits!), specify precision (eg. "int32"/"float32")'
      patterns: [".//Call[func/Attribute[@attr='astype'] and args/Name[@id='{}']]",
                 ".//Call[func/Attribute[@attr='astype'] and keywords/keyword[@arg='dtype']/value/Name[@id='{}']]",
                ]
      template: ["int", "float"]

    - msg: 'WT304: (performance) astype("{}") is not precise enough (default is 64bits!), specify precision (eg. "int32"/"float32")'
      patterns: [ ".//Call[func/Attribute[@attr='astype'] and args/Constant[@type='str' and @value='{}']]",
                  ".//Call[func/Attribute[@attr='astype'] and keywords/keyword[@arg='dtype']/value/Constant[@type='str' and @value='{}']]"]
      template: ["int", "float"]

    - msg: 'WT305: (performance) astype(...) could be merged directly into the read() function in most cases by using out_dtype=...'
      patterns: [ ".//Attribute[@attr='astype']/value/Call/func/Attribute[@attr='read']",]
      template: []

    - msg:  "WT306: (performance) array.max() == 0 probably should be: 'not np.any(array)'"
      patterns: [ ".//Compare[./left//Attribute[@attr='max'] and ./ops/Eq and ./comparators/Constant[@value=0]]",]
      template: []

    - msg: "WT307: (performance) array.max()>0 probably should be: 'np.any(array)'"
      patterns: [ ".//Compare[./left//Attribute[@attr='max'] and ./ops/Gt and ./comparators/Constant[@value=0]]",]
      template: []

    - msg: "WT308: (performance) np.{}(...,0) should be: np.rint(...)"
      patterns: [".//Call[./func/Attribute[@attr='{}' and ./value/Name[@id='numpy' or @id='np']] and ./args/Constant[@value='0']]",]
      template: ['round', 'around']

    - msg: "WT309: (performance) int(A / B) should be written as (A // B) if A and B are integers"
      patterns: [".//Call[./func/Name[@id='int'] and ./args//BinOp/op/Div]",]
      template: []

    - msg: "WT310: (performance) X.{}(): It creates a copy. Use 'ravel()' or rearrange(X, '...->...') from https://github.com/arogozhnikov/einops"
      patterns: [".//Call/func/Attribute[@attr='{}' and ancestor::Call]", ]
      template: ['flatten',]

    - msg: "WT311: (performance) x = np.nan_to_num(x) always makes copy. Use in-place op: x = np.nan_to_num(x, copy=False)"
      patterns: [".//Assign[value/Call/func/Attribute[@attr='nan_to_num']][targets/Name/@id=value/Call/args/Name/@id][count(value/Call/keywords/keyword[@arg='copy'])=0]", ]
      template: []

    - msg: 'WT312: (performance) .zeros(...) is not precise enough, specify dtype!'
      patterns: [".//Call[func/Attribute[@attr='zeros']][count(keywords/keyword[@arg='dtype'])=0]",]

    - msg: 'WT313: (performance) .array(...) is not precise enough, specify dtype!'
      patterns: [".//Call[func/Attribute[@attr='array']][args/List][count(keywords/keyword[@arg='dtype'])=0]",]


    - msg: "WT400: (hint) {} layer: consider using butterfly layer. https://github.com/HazyResearch/butterfly"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['Linear','Dense']

    - msg: "WT401: (hint) Try AdaBelief optimizer instead of {}. See: https://juntang-zhuang.github.io/adabelief/"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['Adam','SGD']

    - msg: "WT402: (hint) Use focal loss instead of cross entropy loss. See: https://arxiv.org/abs/1708.02002"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['CrossEntropyLoss','BinaryCrossEntropy', 'CategoricalCrossEntropy', 'binary_cross_entropy', 'BCELoss', 'categorical_crossentropy']

"""

disabled_rules = """
    - msg: "WT803 PEP20 (Zen of Python) violation. 'Flat is better than nested.' Do you really need a class inside a class?"
      patterns: [".//ClassDef//ClassDef", ]
      template: []

    - msg: "WT804 PEP20 (Zen of Python) violation. 'Flat is better than nested.' Do you really need a class inside a function?"
      patterns: [".//FunctionDef//ClassDef", ]
      template: []

    - msg: "WT800 Document your functions! 'Documentation is a love letter that you write to your future self.' — Damian Conway"
      patterns: [".//FunctionDef/body/*[1]/value/*[(not(self::Constant) or not(string(number(self::Constant/@value))='NaN')) and (preceding::*) and not(ancestor::ClassDef)]", ]
      template: []

    - msg: "WT801 PEP20 (Zen of Python) violation. 'Simple is better than complex.'"
      patterns: [".//FunctionDef[count(./body/*)>40]", ]
      template: []

    - msg: "WT802 PEP20 (Zen of Python) violation. 'Flat is better than nested.' Do you really need a function inside a function?"
      patterns: [".//FunctionDef//FunctionDef", ]
      template: []
"""
