#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Displays a list of states"""
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda x: x.name)
    return render_template('10-states.html', states=sorted_states)


@app.route('/states/<state_id>', strict_slashes=False)
def states_cities(state_id):
    """Displays cities of a specific state"""
    state = storage.get(State, state_id)
    if state:
        cities = sorted(state.cities, key=lambda x: x.name)
        return render_template('10-states_cities.html', state=state, cities=cities)
    else:
        return render_template('10-not_found.html')


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Removes the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
