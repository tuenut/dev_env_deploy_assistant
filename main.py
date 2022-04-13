#!/usr/bin/env python3

import sys
import logging

from argparse import ArgumentParser

from deploy_assistant import DEPLOY_ACTIONS, BUILD_ACTION


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")

    subparsers = parser.add_subparsers(title="Action.", required=True)
    build_action_parser = subparsers.add_parser(BUILD_ACTION)
    build_action_parser.add_argument("next_version", choices=["major", "minor", "patch"], default="minor", required=False)
    build_action_parser.set_defaults(action="build")

    return parser.parse_args()


if __name__ == '__main__':
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format="%(asctime)s: [%(levelname)s]: %(message)s",
    )
    logger = logging.getLogger("deploy-assistant")

    logger.debug("Logger initialized.")
    logger.info("Development environment deploy assistant started.")

    args = parse_args()

    logger.debug(f"Requested action: <{args}>.")

    action_handler = DEPLOY_ACTIONS[args.action]
    action_handler(args)

    logger.info("Done.")

    exit(0)
