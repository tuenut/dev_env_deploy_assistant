import logging
import re
from subprocess import Popen, PIPE
from typing import List, Literal

from semantic_version import Version


logger = logging.getLogger("deploy-assistant.builder")
IMAGE_NAME = "default.dev"
MAJOR_VERSION: str = "major"
MINOR_VERSION = "minor"
PATCH_VERSION = "patch"
_BUILD_VERSIONS_MAP = {
    MAJOR_VERSION: "next_major",
    MINOR_VERSION: "next_minor",
    PATCH_VERSION: "next_patch"
}
BUILD_VERSIONS = tuple(_BUILD_VERSIONS_MAP.keys())


def build_image(args):
    """

    :param args:
        args.major: bool
        args.minor: bool
        args.patch: bool
    :type args: argparse.Namespace

    """
    next_version = _get_next_image_version(args.next_version)

    docker_build_cmd = _get_build_command(
        next_version,
        target="app"  # TODO: see above about `multitarget images`.
    )

    logger.info(f"Execute command: <{docker_build_cmd}>")
    # with Popen(docker_build_cmd, shell=True) as proc:
    #     proc.wait()
    #
    # if proc.returncode != 0:
    #     raise Exception("Something goes wrong on build.")


def _get_next_image_version(
        next_version_type: Literal["major", "minor", "patch"]
) -> Version:
    docker_images_list_cmd = f'docker images {IMAGE_NAME} --format "{{{{.Tag}}}}"'
    logger.info("Execute command: <%s>", docker_images_list_cmd)
    with Popen(docker_images_list_cmd, stdout=PIPE, shell=True) as proc:
        image_tags = proc.stdout.read().decode("utf8").split()

    latest_version = _parse_latest_version(image_tags)
    # TODO: make args to define should be next build is major, minor or patch
    if latest_version:
        logger.info(f"Found latest version of image <{latest_version}>")
        _version_incrementer = getattr(latest_version, _BUILD_VERSIONS_MAP[next_version_type])
        next_version = _version_incrementer()
    else:
        logger.info("Can't find any previous valid versions of image.")
        next_version = Version("0.0.0")

    logger.info(f"Next image version will be <{next_version}>.")

    return next_version


def _parse_latest_version(tags: List[str]) -> Version:
    is_tag_version = re.compile(r"\d+\.\d+(?:\.\d+)?")
    image_tags = map(Version.coerce, filter(is_tag_version.match, tags))
    latest_version = max(image_tags)

    return latest_version


def _get_build_command(
        next_version: Version,
        target: str = None,
        context: str = None
) -> str:
    docker_build_cmd = "docker build"

    image_tag_arg = f"--tag {IMAGE_NAME}"
    version_tag_arg = f"--tag {IMAGE_NAME}:{next_version}"

    cache_from_arg = f"--cache-from {IMAGE_NAME}:latest" \
        if _is_first_version(next_version) else ""

    # TODO: remove multitarget images support until it unified
    target_arg = f"--target {target}" if target else ""

    context_arg = context if context else "."

    cmd = " ".join([
        docker_build_cmd, image_tag_arg, version_tag_arg, cache_from_arg,
        target_arg, context_arg
    ])

    return cmd


def _is_first_version(version: Version) -> bool:
    return version == Version("0.0.0")
