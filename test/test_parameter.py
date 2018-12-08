#test_parameter.py

from pathlib import Path
import sys

root_dir = Path(Path.cwd()).parent

sys.path[0] = str(root_dir)+'/src/'

import pytest

from core import variable
from core import template_units

import copy
