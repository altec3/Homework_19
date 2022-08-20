from flask import Flask

from project.setup.app.config import Config


def app_init(config: Config) -> Flask:

    app = Flask(__name__)
    app.config.from_object(config)
    app.app_context().push()

    return app
