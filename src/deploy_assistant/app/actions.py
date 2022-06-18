from enum import Enum


class Actions(Enum):
    BUILD_ACTION = "build"
    DEPLOY = "deploy"
    UPDATE = "update"
    START = "start"
    STOP = "stop"
    REMOVE = "remove"
