import sys

from loguru import logger

from pathlib import Path

from deploy_assistant.app.options import OptionsParser, Options, Actions
from deploy_assistant.assistant import Assistant


class App:
    opts: Options

    def __init__(self):
        logger.remove()
        self.parser = OptionsParser()

    def run(self):
        self.opts = self.parser.get_options()
        self.__configure_logger()

        logger.info("Development environment deploy assistant started.")
        logger.debug(f"Workdir {Path('.').resolve()}")
        logger.debug(f"Requested action: <{self.opts.action}>.")

        action = Actions.get_action(self.opts)
        Assistant.do(action, self.opts)

        logger.info("Done.")

    def __configure_logger(self):
        logger.add(
            sys.stdout,
            level="DEBUG" if self.opts.debug else "INFO"
        )
