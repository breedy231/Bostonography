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


@app.route('/static/only_a.csv')
def only_a():
    return app.send_static_file('only_a.csv')


@app.route('/static/only_b.csv')
def only_b():
    return app.send_static_file('only_b.csv')


@app.route('/static/only_c.csv')
def only_c():
    return app.send_static_file('only_c.csv')


@app.route('/static/only_a_c.csv')
def only_a_c():
    return app.send_static_file('only_a_c.csv')


@app.route('/static/only_a_b.csv')
def only_a_b():
    return app.send_static_file('only_a_b.csv')


@app.route('/static/only_a_b_c.csv')
def only_a_b_c():
    return app.send_static_file('only_a_b_c.csv')

@app.route('/dist/leaflet.awesome-markers.css')
def markers():
    return app.send_static_file('leaflet.awesome-markers.css')

@app.route('/dist/leaflet.awesome-markers.js')
def markersscript():
    return app.send_static_file('leaflet.awesome-markers.js')

@app.route('/dist/images/markers-soft.png')
def markerssoft():
    return app.send_static_file('markers-soft.png')

@app.route('/dist/images/markers-shadow.png')
def markerssoft():
    return app.send_static_file('markers-shadow.png')


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
