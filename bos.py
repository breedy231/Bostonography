# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify
from flask_navigation import Navigation


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
nav = Navigation()
nav.init_app(app)


# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

nav.Bar('top', [
    nav.Item('Home', 'index'),
    nav.Item('Alejandro', 'alejandro'),
    nav.Item('Brendan', 'brendan'),
    nav.Item('Doug', 'doug'),

])


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/brendan')
def brendan():
    return render_template('brendan.html')


@app.route('/alejandro')
def alejandro():
    return render_template('alejandro.html')


@app.route('/doug')
def doug():
    return render_template('doug.html')

@app.route('/static/rest_true.csv')
def rest_true():
    return app.send_static_file('rest_true.csv')


if __name__ == '__main__':
     app.debug = True
     port = int(os.environ.get("PORT", 5000))
     app.run(host='0.0.0.0', port=port)
