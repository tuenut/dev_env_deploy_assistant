from .build import build_image
from .deploy import deploy_services
from .remove import remove_environment
from .start import start_environment
from .stop import stop_environment
from .update import update_services


try:
    import semantic_version
except ImportError:
    print("Please install semantic-version via `pip3 install semantic-version`.")
    exit(1)
else:
    from semantic_version import Version

BUILD_ACTION = "build"
DEPLOY = "deploy"
UPDATE = "update"
START = "start"
STOP = "stop"
REMOVE = "remove"
DEPLOY_ACTIONS = {
    BUILD_ACTION: build_image,
    DEPLOY: deploy_services,
    UPDATE: update_services,
    "up": update_services,
    START: start_environment,
    STOP: stop_environment,
    REMOVE: remove_environment,
    "rm": remove_environment,
}


