#!/usr/bin/env python
"""Define the basic (Function) Approximator class.

This file describes the `Approximator` class that wraps a learning model and connects it with its inputs, and outputs.
The inputs/outputs can be states, actions, arrays/tensors, etc.

Dependencies:
- `pyrobolearn.models`
- `pyrobolearn.states`
- `pyrobolearn.actions`
"""

import collections
import numpy as np
import torch

from pyrobolearn.states import State
from pyrobolearn.actions import Action
from pyrobolearn.models import Model
from pyrobolearn.processors import Processor


__author__ = "Brian Delhaisse"
__copyright__ = "Copyright 2018, PyRoboLearn"
__credits__ = ["Brian Delhaisse"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Brian Delhaisse"
__email__ = "briandelhaisse@gmail.com"
__status__ = "Development"


class Approximator(object):
    r"""Function Approximator (abstract) class

    The function approximator is a wrapper around the inner learning base model, and connects a learning model to
    its state / action inputs and outputs. That is, this class described how to connect a learning model with
    states / actions, and thus allows the inner models to be independent from the notions of states and actions.

    This class and all the children inheriting from this one will be used internally by several classes such as
    policies, dynamic models, value estimators, and others. This enables to not duplicate and write the same code
    for these various different concepts which share similar features. For instance, policies are function
    approximators where the inputs are states, and the outputs are actions while dynamic transition models are
    approximators where the inputs are states and actions, and the outputs are the next state.

    Often the learning model can be constructed automatically by knowing the input and output dimensions, along with
    few other optional parameters. This is useful if one does not wish to change the learning model but just to scale
    it to different input/output sizes.

    This class is used by the following classes:
    * Policy: approximator mapping states to actions
    * Value estimator: approximator mapping states (or states and actions) to a value, or mapping states to actions
                       (in the case of discrete actions)
    * Actor-Critic: combination of policy and value function approximators
    * Dynamic: approximator mapping states and actions to the next states
    * Transformation mappings: approximator mapping states to states
    """

    def __init__(self, inputs, outputs, model=None, preprocessors=None, postprocessors=None):
        r"""Initialize the outer model.

        Args:
            inputs (State, Action, np.array, torch.Tensor): inputs of the inner models (instance of State/Action)
            outputs (State, Action, np.array, torch.Tensor): outputs of the inner models (instance of Action/State)
            model (Model, None): inner model which will be wrapped if not an instance of Model
            preprocessors (None, Processor, list of Processor): the inputs are first given to the preprocessors then
                to the model.
            postprocessors (None, Processor, list of Processor): the predicted outputs by the model are given to the
                processors before being returned.
        """

        # Check inputs and outputs, and convert to the correct format
        self._model = None
        self.inputs = inputs
        self.outputs = outputs

        # set pre- and post- processors
        self.preprocessors = preprocessors
        self.postprocessors = postprocessors

        # Check the given model: check if correct input/output sizes wrt the previous arguments, and check
        # the model type and wrap it if necessary. That is, if the type is from the original module/library,
        # wrap it with the corresponding inner model
        self.model = model

    ##############
    # Properties #
    ##############

    @property
    def inputs(self):
        """Return the approximator's inputs."""
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        """Set the approximator's inputs."""
        if inputs is not None:
            if isinstance(inputs, (int, float)):
                inputs = np.array([inputs])
            elif not isinstance(inputs, (State, Action, torch.Tensor, np.ndarray)):
                raise TypeError("Expecting the inputs to be a State, Action, torch.Tensor, or np.ndarray.")
            if self._model is not None:
                pass  # TODO: check that the dimensions agree with the model
        # set inputs
        self._inputs = inputs

    @property
    def outputs(self):
        """Return the approximator's outputs."""
        return self._outputs

    @outputs.setter
    def outputs(self, outputs):
        """Set the approximator's outputs."""
        if outputs is not None:
            if isinstance(outputs, (int, float)):
                outputs = np.array([outputs])
            elif not isinstance(outputs, (State, Action, torch.Tensor, np.ndarray)):
                raise TypeError("Expecting the outputs to be a State, Action, torch.Tensor, or np.ndarray.")
            if self._model is not None:
                pass  # TODO: check that the dimensions agree with the model
        # set outputs
        self._outputs = outputs

    @property
    def model(self):
        """Return the inner learning model."""
        return self._model

    @model.setter
    def model(self, model):
        """Set the inner learning model."""
        if model is not None:
            # check model type
            # if not isinstance(model, Model):
            #     raise TypeError("Expecting the model to be an instance of Model, instead received: "
            #                     "{}".format(type(model)))
            # TODO

            # check model input/output shape
            if self._inputs is None:
                raise ValueError("Inputs have not been set.")
            if self._outputs is None:
                raise ValueError("Outputs have not been set.")
            shape = model.input_shape

            # TODO

        # set model
        self._model = model

    @property
    def preprocessors(self):
        """Return the list of pre-processors."""
        return self._preprocessors

    @preprocessors.setter
    def preprocessors(self, processors):
        """Set the list of pre-processors."""
        if processors is None:
            processors = []
        elif callable(processors):
            processors = [processors]
        elif isinstance(processors, collections.Iterable):
            for idx, processor in enumerate(processors):
                if not callable(processor):
                    raise ValueError("The {} processor {} is not callable.".format(idx, processor))
        else:
            raise TypeError("Expecting the processors to be None, a callable class / function such as `Processor`, "
                            "or a list of them. Instead got: {}".format(type(processors)))
        self._preprocessors = processors

    @property
    def postprocessors(self):
        """Return the list of post-processors."""
        return self._postprocessors

    @postprocessors.setter
    def postprocessors(self, processors):
        """Set the list of post-processors."""
        if processors is None:
            processors = []
        elif callable(processors):
            processors = [processors]
        elif isinstance(processors, collections.Iterable):
            for idx, processor in enumerate(processors):
                if not callable(processor):
                    raise ValueError("The {} processor {} is not callable.".format(idx, processor))
        else:
            raise TypeError("Expecting the processors to be None, a callable class / function such as `Processor`, "
                            "or a list of them. Instead got: {}".format(type(processors)))
        self._postprocessors = processors

    @property
    def input_size(self):
        """Return the approximator input size."""
        return self.model.input_size

    @property
    def output_size(self):
        """Return the approximator output size."""
        return self.model.output_size

    @property
    def input_shape(self):
        """Return the approximator input shape."""
        return self.model.input_shape

    @property
    def output_shape(self):
        """Return the approximator output shape."""
        return self.model.output_shape

    @property
    def input_dim(self):
        """Return the input dimension."""
        return self.model.input_dim

    @property
    def output_dim(self):
        """Return the output dimension."""
        return self.model.output_dim

    @property
    def num_parameters(self):
        """Return the total number of parameters of the inner learning model."""
        return self.model.num_parameters

    @property
    def num_hyperparameters(self):
        """Return the total number of hyper-parameters of the inner learning model."""
        return self.model.num_hyperparameters

    ###########
    # Methods #
    ###########

    def is_parametric(self):
        """
        Return True if the model is parametric.

        Returns:
            bool: True if the model is parametric.
        """
        return self.model.is_parametric()

    def is_linear(self):
        """
        Return True if the model is linear (wrt the parameters). This can be for instance useful for some learning
        algorithms (some only works on linear models).

        Returns:
            bool: True if it is a linear model
        """
        return self.model.is_linear()

    def is_recurrent(self):
        """
        Return True if the model is recurrent. This can be for instance useful for some learning algorithms which
        change their behavior when they deal with recurrent learning models.

        Returns:
            bool: True if it is a recurrent model.
        """
        return self.model.is_recurrent()

    def is_deterministic(self):
        """
        Return True if the model is deterministic.

        Returns:
            bool: True if the model is deterministic.
        """
        return self.model.is_deterministic()

    def is_probabilistic(self):
        """
        Return True if the model is probabilistic/stochastic.

        Returns:
            bool: True if the model is probabilistic.
        """
        return self.model.is_probabilistic()

    # alias
    is_stochastic = is_probabilistic

    def is_discriminative(self):
        """
        Return True if the model is discriminative, that is, if the model estimates the conditional probability
        :math:`p(y|x)`.

        Returns:
            bool: True if the model is discriminative.
        """
        return self.model.is_discriminative()

    def is_generative(self):
        """
        Return True if the model is generative, that is, if the model estimates the joint distribution of the input
        and output :math:`p(x,y)`. A generative model allows to sample from it.

        Returns:
            bool: True if the model is generative.
        """
        return self.model.is_generative()

    def _size(self, x):
        """Return the total size of a `State`, `Action`, numpy.array, or torch.Tensor."""
        size = 0
        if isinstance(x, (State, Action)):
            if x.is_discrete():
                size = x.space[0].n
            else:
                size = x.total_size()
        elif isinstance(x, np.ndarray):
            size = x.size
        elif isinstance(x, torch.Tensor):
            size = x.numel()
        elif isinstance(x, int):
            size = x
        return size

    def parameters(self):
        """Return an iterator over the approximator parameters."""
        return self.model.parameters()

    def named_parameters(self):
        """Return an iterator over the approximator parameters, yielding both the name and the parameter itself."""
        return self.model.named_parameters()

    def list_parameters(self):
        """Return the list of parameters."""
        return list(self.parameters())

    def hyperparameters(self):
        """Return an iterator over the approximator hyper-parameters."""
        return self.model.hyperparameters()

    def named_hyperparameters(self):
        """Return an iterator over the approximator hyper-parameters, yielding both the name and the hyper-parameter
        itself."""
        return self.model.named_hyperparameters()

    def list_hyperparameters(self):
        """Return the list of hyper-parameters."""
        return list(self.hyperparameters())

    def get_vectorized_parameters(self, to_numpy=True):
        """Return a vectorized form of the parameters"""
        return self.model.get_vectorized_parameters(to_numpy=to_numpy)

    def set_vectorized_parameters(self, vector):
        """Set the vector parameters."""
        self.model.set_vectorized_parameters(vector=vector)

    def reset(self, reset_processors=False):
        """Reset the approximators."""
        if reset_processors:
            for processor in self.preprocessors:
                if isinstance(processor, Processor):
                    processor.reset()
            for processor in self.postprocessors:
                if isinstance(processor, Processor):
                    processor.reset()
        self.model.reset()

    def predict(self, x=None, to_numpy=True, return_logits=False):
        """Predict the output given the input."""
        # if no input is given, take the provided inputs at the beginning
        if x is None:
            x = self.inputs

        # if the input is an instance of State or Action, get the inner merged data.
        if isinstance(x, (State, Action)):
            x = x.merged_data
            if len(x) == 1:
                x = x[0]

        # go through each preprocessor
        for processor in self.preprocessors:
            x = processor(x)

        # go through the model
        x = self.model.predict(x, to_numpy=False)

        # go through each postprocessor
        for processor in self.postprocessors:
            x = processor(x)

        # set the output data
        if isinstance(self.outputs, (State, Action)):  # TODO: think when multiple outputs and to set them
            if self.outputs.is_discrete() and not return_logits:
                if isinstance(x, np.ndarray):
                    x = np.array([np.argmax(x)])
                elif isinstance(x, torch.Tensor):
                    x = torch.argmax(x, dim=0, keepdim=True)
                else:
                    raise TypeError("Expecting `x` to be a numpy array, torch.Tensor, or a list of them, instead got: "
                                    "{}".format(type(x)))

            # set the data
            if isinstance(x, np.ndarray):
                self.outputs.data = x
            else:  # isinstance(x, torch.Tensor):
                self.outputs.torch_data = x

        # return the data
        # convert to numpy if specified
        if to_numpy and isinstance(x, torch.Tensor):
            if x.requires_grad:
                return x.detach().numpy()
            return x.numpy()
        return x

    def save(self, filename):
        """save the inner model."""
        self.model.save(filename)

    def load(self, filename):
        """load the inner model."""
        self.model.load(filename)

    #############
    # Operators #
    #############

    def __call__(self, x):
        """Predict the output using the inner learning model given the input."""
        return self.predict(x)

    def __repr__(self):
        """Return a representation of the model."""
        return self.model.__str__()

    def __str__(self):
        """Return a string describing the model."""
        return self.model.__str__()


# Tests
if __name__ == '__main__':
    pass