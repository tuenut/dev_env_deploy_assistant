#!/usr/bin/env python3

import sys
from loguru import logger

from assistant import DEPLOY_ACTIONS
from options import OptionsParser


if __name__ == '__main__':
    logger.remove()

    opts = OptionsParser().get_options()

    logger.add(sys.stdout, level="DEBUG" if opts.verbose else "INFO")
    logger.debug("Development environment deploy assistant started.")

    logger.debug(f"Requested action: <{opts}>.")

    action_handler = DEPLOY_ACTIONS[opts.action]
    action_handler(opts)

    logger.info("Done.")

    exit(0)
