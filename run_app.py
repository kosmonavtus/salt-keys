from app_salt_keys.main import app
from app_salt_keys.config import GunicornSettings
from gunicorn.app.base import BaseApplication


class FlaskApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def run_gunicorn(app):
    FlaskApplication(app, GunicornSettings()).run()


if __name__ == '__main__':
    run_gunicorn(app)
