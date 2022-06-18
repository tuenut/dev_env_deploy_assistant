from deploy_assistant.assistant.build import build_image
from deploy_assistant.assistant.deploy import deploy_services
from deploy_assistant.assistant.remove import remove_environment
from deploy_assistant.assistant.start import start_environment
from deploy_assistant.assistant.stop import stop_environment
from deploy_assistant.assistant.update import update_services
from deploy_assistant.app.actions import Actions


DEPLOY_ACTIONS = {
    Actions.BUILD: build_image,
    Actions.DEPLOY: deploy_services,
    Actions.UPDATE: update_services,
    Actions.START: start_environment,
    Actions.STOP: stop_environment,
    Actions.REMOVE: remove_environment,
}


