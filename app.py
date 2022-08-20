from project.setup.app.app_init import app_init
from project.setup.app.app_configure import configure_app
from project.setup.db.db_utils import create_db, fill_db
from project.setup.app.config import Config

app_config = Config()

app = app_init(app_config)
configure_app(app)

create_db(app)
fill_db(app)


if __name__ == "__main__":
    app.run()
