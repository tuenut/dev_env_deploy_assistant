from __future__ import annotations

import re

from loguru import logger

from subprocess import Popen, PIPE
from typing import List, Literal

from semantic_version import Version

from deploy_assistant.app.options import Options


_BUILD_VERSIONS_MAP = {
    "major": "next_major",
    "minor": "next_minor",
    "patch": "next_patch"
}


class ImageBuilder:
    def __init__(self, options: Options):
        self.options = options

        self.target = "app"
        self.context = "."

    def build_image(self):
        new_image_version = self._get_new_image_version()
        self._build_image(new_image_version)

    def _build_image(self, image_version: Version):
        build_cmd = self.__get_build_command(image_version)
        logger.info(f"Execute command: `{build_cmd}`")

        if self.options.simulate:
            return

        with Popen(build_cmd, shell=True) as proc:
            proc.wait()

        if proc.returncode != 0:
            raise Exception("Something goes wrong on build.")

    def _get_new_image_version(self) -> Version:
        # TODO: make args to define which should be next build is major,
        #  minor or patch
        image_tags = self.__get_docker_images()

        try:
            latest_version = self._parse_latest_version(image_tags)
        except ValueError:
            new_version = self.__get_default_version()
        else:
            new_version = self.__get_next_version(latest_version)

        logger.info(f"Next image version will be <{new_version}>.")

        return new_version

    def __get_docker_images(self):
        docker_images_list_cmd = \
            f'docker images {self.options.image} --format "{{{{.Tag}}}}"'
        logger.info(f"Execute command: `{docker_images_list_cmd}`", )
        with Popen(docker_images_list_cmd, stdout=PIPE, shell=True) as proc:
            image_tags = proc.stdout.read().decode("utf8").split()

        return image_tags

    def __get_next_version(self, latest_version):
        logger.info(f"Found latest version of image <{latest_version}>")
        _version_incrementer = getattr(
            latest_version,
            _BUILD_VERSIONS_MAP[self.options.next_version]
        )
        return _version_incrementer()

    def __get_default_version(self):
        logger.info("Can't find any previous valid versions of image.")
        return Version("0.0.0")

    def __get_build_command(self, new_image_version: Version) -> str:
        docker_build_cmd = "docker build"

        image_tag_arg = f"--tag {self.options.image}"
        version_tag_arg = f"--tag {self.options.image}:{new_image_version}"

        cache_from_arg = f"--cache-from {self.options.image}:latest" \
            if not self._is_first_version(new_image_version) else ""

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
