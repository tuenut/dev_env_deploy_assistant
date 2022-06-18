from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Literal

from .deploy_assistant import BUILD_ACTION


@dataclass
class Options:
    verbose: bool
    simulate: bool
    action: str
    image: str = None
    next_version: Literal["major", "minor", "patch"] = None


class OptionsParser:
    def __init__(self):
        self.parser = ArgumentParser(
            prog="deploy_assistant",
            description="That program helps you to manage your app images at "
                        "your local dev environment. For now you can build and "
                        "rebuild images, and deploy assistant will control image "
                        "version."
        )
        self.parser.add_argument("-v", "--verbose", action="store_true")
        self.parser.add_argument("-s", "--simulate", "--dry-run", "--no-act", action="store_true")

        self.__add_build_action()

    def __add_build_action(self):
        subparsers = self.parser.add_subparsers(title="Action", required=True)

        build_action_parser = subparsers.add_parser(BUILD_ACTION)
        build_action_parser.add_argument("image")
        build_action_parser.add_argument("next_version", choices=["major", "minor", "patch"], default="minor")
        build_action_parser.set_defaults(action="build")

    def get_options(self) -> Options:
        namespace = self.parser.parse_args()
        opts = Options(**dict(namespace._get_kwargs()))

        return opts
