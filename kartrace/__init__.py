import os

from flask import Flask

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'kartrace.sqlite'),
    )

    if test_config is None:
        #load the instace config, if exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load the test config if passed in
        app.config.from_mapping(test_config)

    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello

    @app.route('/hello')
    def hello():
        return 'Hello, World'

    from . import db
    db.init_app(app)

    from . import race
    app.register_blueprint(race.bp)

    from . import nav
    app.register_blueprint(nav.bp)
    app.add_url_rule('/', endpoint='index')

    from . import year
    app.register_blueprint(year.bp)

    return app