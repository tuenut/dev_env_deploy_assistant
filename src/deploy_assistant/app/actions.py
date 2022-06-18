from enum import Enum


class Actions(Enum):
    BUILD = "build"
    DEPLOY = "deploy"
    UPDATE = "update"
    START = "start"
    STOP = "stop"
    REMOVE = "remove"
