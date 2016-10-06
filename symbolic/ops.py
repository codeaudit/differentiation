from __future__ import print_function
from __future__ import division

import numpy as np

class BaseOp(object):
    """
    Represents a graph node that performs computation on tensors.
    For simplicity, every op has an array of N inputs and a M=1 outputs.
    """

    def __init__(self, inputs, graph=None, name=None):
        self.inputs = [graph.convert(input_) for input_ in inputs]
        self.output = graph.tensor(op=self, name=name+':0' if name is not None else 'None:0')
        self.graph = graph
        self.name = name

    def compute(self, context):
        raise NotImplementedError()

    def gradient(self, grad):
        # grad: N Tensor objects (grad w.r.t. each output)
        # return: M Tensor objects (partial grad w.r.t. each input)
        raise NotImplementedError()

    def __str__(self):
        return '{}("{}")'.format(type(self).__name__, self.name)

    def __repr__(self):
        return str(self)

class AddOp(BaseOp):

    def __init__(self, inputs, graph=None, name='Add'):
        super(AddOp, self).__init__(inputs, graph, name)

    def compute(self, context):
        a, b = self.inputs
        return context[a] + context[b]

    def gradient(self, grad):
        return [grad, grad]

class SubOp(BaseOp):

    def __init__(self, inputs, graph=None, name='Sub'):
        super(SubOp, self).__init__(inputs, graph, name)

    def compute(self, context):
        a, b = self.inputs
        return context[a] - context[b]

    def gradient(self, grad):
        return [grad, -grad]

class MulOp(BaseOp):

    def __init__(self, inputs, graph=None, name='Mul'):
        super(MulOp, self).__init__(inputs, graph, name)

    def compute(self, context):
        a, b = self.inputs
        return context[a] * context[b]

    def gradient(self, grad):
        a, b = self.inputs
        return [b * grad, a * grad]

class DivOp(BaseOp):

    def __init__(self, inputs, graph=None, name='Div'):
        super(DivOp, self).__init__(inputs, graph, name)

    def compute(self, context):
        a, b = self.inputs
        return context[a] / context[b]

    def gradient(self, grad):
        a, b = self.inputs
        return [grad / b, grad * (-a / self.graph.square(y))]

class SquareOp(BaseOp):

    def __init__(self, inputs, graph=None, name='Square'):
        super(SquareOp, self).__init__(inputs, graph, name)

    def compute(self, context):
        input_, = self.inputs
        return context[input_]**2

    def gradient(self, grad):
        return [2 * self.inputs[0] * grad]

class GradientOp(BaseOp):

    def __init__(self, y, x, graph=None, name=None):
        super(GradientOp, self).__init__([y], graph, 'grad_'+x.name)
        self.y = y
        self.x = x

    def partial(self, y, grad_y, gradients, context):
        gradients[y] = grad_y.eval(context)

        if y.op is None:
            return

        inputs = y.op.inputs
        grad_ys_inputs = y.op.gradient(grad_y)
        assert len(inputs) == len(grad_ys_inputs)

        for input_, grad_y_input in zip(inputs, grad_ys_inputs):
            self.partial(input_, grad_y_input, gradients, context)

    def compute(self, context):
        print('Computing the derivative of {} w.r.t. {}...'.format(self.y, self))
        gradients = {}
        self.partial(self.y, self.graph.convert(1), gradients, context)
        return gradients[self.x]

    def gradient(self, grad):
        raise NotImplementedError()