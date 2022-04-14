import logging
import re
from subprocess import Popen, PIPE
from typing import List, Literal

from semantic_version import Version


logger = logging.getLogger("deploy-assistant.builder")

_BUILD_VERSIONS_MAP = {
    "major": "next_major",
    "minor": "next_minor",
    "patch": "next_patch"
}
BUILD_VERSIONS = tuple(_BUILD_VERSIONS_MAP.keys())


class ImageBuilder:
    _next_version: Version
    _build_cmd: str

    __simulate: bool
    __update_type: Literal["major", "minor", "patch"]
    __image: str

    def __init__(self, args):
        self.__simulate = args.simulate
        self.__update_type = args.next_version
        self.__image = args.image

        self.target = "app"
        self.context = "."

    def build_image(self):
        self._next_version = self.__next_image_version
        self._build_cmd = self.__build_command

        logger.info(f"Execute command: `{self._build_cmd}`")

        if self.__simulate:
            return

        self._build_image()

    def _build_image(self):
        with Popen(self.__build_command, shell=True) as proc:
            proc.wait()

        if proc.returncode != 0:
            raise Exception("Something goes wrong on build.")

    @property
    def __next_image_version(self) -> Version:
        docker_images_list_cmd = f'docker images {self.__image} --format "{{{{.Tag}}}}"'
        logger.info("Execute command: `%s`", docker_images_list_cmd)
        with Popen(docker_images_list_cmd, stdout=PIPE, shell=True) as proc:
            image_tags = proc.stdout.read().decode("utf8").split()

        self.latest_version = self._parse_latest_version(image_tags)
        # TODO: make args to define should be next build is major, minor or patch
        if self.latest_version:
            logger.info(f"Found latest version of image <{self.latest_version}>")
            _version_incrementer = getattr(
                self.latest_version,
                _BUILD_VERSIONS_MAP[self.__update_type]
            )
            next_version = _version_incrementer()
        else:
            logger.info("Can't find any previous valid versions of image.")
            next_version = Version("0.0.0")

        logger.info(f"Next image version will be <{next_version}>.")

        return next_version

    @property
    def __build_command(self) -> str:
        docker_build_cmd = "docker build"

        image_tag_arg = f"--tag {self.__image}"
        version_tag_arg = f"--tag {self.__image}:{self._next_version}"

        cache_from_arg = f"--cache-from {self.__image}:latest" \
            if self._is_first_version(self._next_version) else ""

        # TODO: remove multitarget images support until it unified
        target_arg = f"--target {self.target}"

        cmd = " ".join([
            docker_build_cmd, image_tag_arg, version_tag_arg, cache_from_arg,
            target_arg, self.context
        ])

        return cmd

    @staticmethod
    def _parse_latest_version(tags: List[str]) -> Version:
        is_tag_version = re.compile(r"\d+\.\d+(?:\.\d+)?")
        image_tags = map(Version.coerce, filter(is_tag_version.match, tags))
        latest_version = max(image_tags)

        return latest_version

    @staticmethod
    def _is_first_version(version: Version) -> bool:
        return version == Version("0.0.0")


def build_image(args):
    builder = ImageBuilder(args)
    builder.build_image()
