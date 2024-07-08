#!/usr/bin/env python

# For details: https://github.com/arnaizaitor/pyguts/blob/main/LICENSE
# Copyright (c) https://github.com/arnaizaitor/pyguts/blob/main/CONTRIBUTORS.txt

# pylint: disable=import-outside-toplevel
import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir)
    ),
)

import pyguts
from pyguts.logger.logger import logger  # noqa: E402

logger.info("Running pyguts. Modifying system path...")
pyguts.set_guts_path()

logger.info("Running pyguts...")
pyguts.run_pyguts()