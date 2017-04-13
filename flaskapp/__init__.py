import click
from os import path
from flask import Flask
from flask_security import Security, PeeweeUserDatastore
# First-party imports
from . import admin
from . import models


def create_app():
    """Creates an app, loads default config from this module and optionally overrides
    it from the file pointed to by the 'FLASKAPP_SETTINGS' environment variable.
    """
    app = Flask(__name__)
    # first read config from this module
    app.config.from_object(__name__)
    # update by overriding some values
    app.config.update(dict(
        DATABASE='sqlite:///'+path.join(app.root_path, 'flaskapp.db'),
        SECRET_KEY='development key',
        USERNAME='admin',
        PASSWORD='default',
        # Set config values for Flask-Security.
        # We're using PBKDF2 with salt.
        SECURITY_PASSWORD_HASH='pbkdf2_sha512',
        SECURITY_PASSWORD_SALT='thisistherhythmofthenightoooohaaaoooow'
    ))
    # finally, read from a file in the environment
    app.config.from_envvar('FLASKAPP_SETTINGS', silent=True)

    # initialise the database, the database url is read from the app config
    models.db.init_app(app)

    # initialise the administrative interface
    admin.init_app(app)
    return app


app = create_app()
user_datastore = PeeweeUserDatastore(models.db, models.User, models.Role, models.UserRoles)
security = Security(app, user_datastore)


@app.before_first_request
def before_first_request():
    """Function executed before the first requests. Ensures an admin is present."""
    with models.db.database.atomic():
        user_datastore.find_or_create_role(name='admin', description='Administrator')
        if not user_datastore.get_user('admin@flaskapp.com'):
            user_datastore.create_user(email='admin@flaskapp.com', name='admin',
                                       password='password')

    with models.db.database.atomic():
        user_datastore.add_role_to_user('admin@flaskapp.com', 'admin')

    models.db.close_db(exc=None)


@app.cli.command('initdb', short_help='Initialise the database')
def cmd_initdb():
    click.echo("initialise the db")
    with app.app_context():
        models.initdb()


if __name__ == '__main__':
    app.run()
