#!/usr/bin/env python
r"""Provide the capture point constraint.


The implementation of this class is inspired by [1] (which is licensed under the LGPLv2).

References:
    - [1] "OpenSoT: A whole-body control library for the compliant humanoid robot COMAN", Rocchi et al., 2015
"""

import numpy as np

from pyrobolearn.priorities.constraints.constraint import Constraint


__author__ = "Brian Delhaisse"
__copyright__ = "Copyright 2019, PyRoboLearn"
__credits__ = ["Enrico Mingo Hoffman (C++)", "Brian Delhaisse (Python + doc)"]
__license__ = "GNU GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Brian Delhaisse"
__email__ = "briandelhaisse@gmail.com"
__status__ = "Development"


class CapturePointConstraint(Constraint):
    r"""Capture Point constraint.

    """

    def __init__(self, model):
        super(CapturePointConstraint, self).__init__(model)
