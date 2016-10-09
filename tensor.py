from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import numpy as np

class Tensor(object):
    """Tensor represents a value in a Graph."""

    def __init__(self, value, shape, op, graph, name):
        if isinstance(value, list):
            self.value = np.array(value)
        else:
            self.value = value

        if shape is None:
            if self.value is not None and isinstance(self.value, np.ndarray):
                self.shape = self.value.shape
            else:
                self.shape = (1,)
        else:
            self.shape = shape

        if name is None:
            self.name = 'Tensor'
        else:
            self.name = name

        self.graph = graph
        self.op = op

        assert not isinstance(self.value, Tensor)
        assert hasattr(self, 'graph') and self.graph is not None
        assert hasattr(self, 'shape') and self.shape is not None
        assert hasattr(self, 'name') and self.name is not None

    def __add__(self, other):
        return self.graph.add(self, other)

    def __sub__(self, other):
        return self.graph.sub(self, other)

    def __mul__(self, other):
        return self.graph.mul(self, other)

    def __div__(self, other):
        return self.graph.div(self, other)

    def __truediv__(self, other):
        return self.graph.div(self, other)

    def __neg__(self):
        return self.graph.neg(self)

    def __radd__(self, other):
        return self.graph.add(other, self)

    def __rsub__(self, other):
        return self.graph.sub(other, self)

    def __rmul__(self, other):
        return self.graph.mul(other, self)

    def __rdiv__(self, other):
        return self.graph.div(other, self)

    def __rtruediv__(self, other):
        return self.graph.div(other, self)

    def __repr__(self):
        return '{}("{}", shape={})'.format(type(self).__name__, self.name, self.shape)