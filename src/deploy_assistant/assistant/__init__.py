from deploy_assistant.app.options import Actions
from deploy_assistant.assistant.build import ImageBuilder


__all__ = ["Assistant"]


class Assistant:
    @classmethod
    def do(cls, action: Actions, options):
        handler = cls.HANDLERS[action]
        return handler(options)

    @staticmethod
    def not_implemented(*args, **kwargs):
        raise NotImplementedError("Action not implemented!")

    @staticmethod
    def build_image(options):
        builder = ImageBuilder(options)
        builder.build_image()

    HANDLERS = {
        Actions.BUILD: build_image,
        Actions.SET: not_implemented,
        Actions.RESET: not_implemented,
        Actions.LIST: not_implemented,
        Actions.PURGE: not_implemented,
    }
