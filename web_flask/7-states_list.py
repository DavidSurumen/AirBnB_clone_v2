#!/usr/bin/python3
""" Flask app which lists all State objects
"""
from flask import Flask, render_template
from models.state import State
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states_list')
def all_states():
    """ display in html, list of states """
    state_list = storage.all(State)
    return render_template('7-states_list.html', states=state_list)


@app.teardown_appcontext
def tearDown(self):
    """ removes the current sqlalchemy session. """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
