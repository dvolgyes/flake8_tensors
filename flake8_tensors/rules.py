rules_yaml = """
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


    - msg: "WT108 np.{}: use bottleneck instead of numpy! Check out: https://github.com/pydata/bottleneck"
      patterns: [".//Call/func/Attribute[(value/Name/@id='np' or value/Name/@id='numpy') and @attr='{}']", ]
      template: ["nansum", "nanmean", "nanstd", "nanvar", "nanmin", "nanmax", "median", "nanmedian", "ss", "nanargmin", "nanargmax", "anynan", "allnan", "rankdata", "nanrankdata", "partition", "argpartition", "replace", "push", "move_sum", "move_mean", "move_std", "move_var", "move_min", "move_max", "move_argmin", "move_argmax", "move_median", "move_rank"]

    - msg: "WT109 np.any(np.isnan(x)): use bn.anynan(x) from bottleneck, it is much faster! https://github.com/pydata/bottleneck"
      patterns: [".//Call[((func/Attribute/value/Name/@id='np' or func/Attribute/value/Name/@id='numpy') and func/Attribute/@attr='any') and args/Call/func/Attribute[(value/Name/@id='np' or value/Name/@id='numpy') and @attr='isnan']]", ]
      template: []

    - msg: "WT110 np.all(np.isnan(x)): use bn.allnan(x) from bottleneck, it is much faster! https://github.com/pydata/bottleneck"
      patterns: [".//Call[((func/Attribute/value/Name/@id='np' or func/Attribute/value/Name/@id='numpy') and func/Attribute/@attr='all') and args/Call/func/Attribute[(value/Name/@id='np' or value/Name/@id='numpy') and @attr='isnan']]", ]
      template: []

    - msg: "WT111 np.{}: do you really need an isnan? Can't you use nansum/nanmean/nan* functions? Check out: https://github.com/pydata/bottleneck"
      patterns: [".//Call/func/Attribute[(value/Name/@id='np' or value/Name/@id='numpy') and @attr='{}' and not(ancestor::Call/func/Attribute[(value/Name/@id='np' or value/Name/@id='numpy') and (@attr='any' or @attr='all')]) ]", ]
      template: ["isnan"]

    - msg: "WT112 .{}() calls also need to assign to a new variable, they do NOT change their underlying variable"
      patterns: [".//Expr/value/Call/func/Attribute[@attr='{}']", ]
      template: ['cpu', 'detach', 'permute','view','reshape','transpose','flatten','ravel','unravel','squeeze','unsqueeze','chunk','stack', 'concatenate','cat','dstack','hstack','vstack']



    - msg: "WT200 Beware with Pytorch's DropOut2d/DropOut3d! They ALWAYS drop 2nd dimension ONLY."
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['DropOut2d','DropOut3d', 'dropout2d','dropout3d']

    - msg: "WT201 Beware: {} has affine=False as default, unlike in BatchNorm and GroupNorm! Set 'affine' explicitly. See: https://github.com/pytorch/pytorch/issues/22755"
      patterns: [".//Name[@id='{}' and ancestor::Call and not(../../keywords//@arg='affine')]", ".//Attribute[@attr='{}' and ancestor::Call and not(../../keywords//@arg='affine')]"]
      template: ['InstanceNorm1d','InstanceNorm2d','InstanceNorm3d']

    - msg: "WT300 torch.nn.X: use nn.X. Shorter code is more readable."
      patterns: [".//Name[@id='torch' and ../../../Attribute/@attr='nn' and not(ancestor::Import or ancestor::ImportFrom)]",]
      template: [ ]

    - msg: "WT301 .clone(): use .copy() for numpy-compatible names (Pytorch 1.7+)"
      patterns: [".//Call/func/Attribute[@attr='clone']",]
      template: ['clone']

    - msg: "WT400 {} layer: consider using butterfly layer. https://github.com/HazyResearch/butterfly"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['Linear','Dense']

    - msg: "WT401 Try AdaBelief optimizer instead of {}. See: https://juntang-zhuang.github.io/adabelief/"
      patterns: [".//Name[@id='{}' and ancestor::Call]", ".//Attribute[@attr='{}' and ancestor::Call]"]
      template: ['Adam','SGD']

    - msg: "WT402 Use focal loss instead of cross entropy loss. See: https://arxiv.org/abs/1708.02002"
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
