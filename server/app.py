# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_by_id(id):
    earthquakes = Earthquake.query.filter(Earthquake.id == id).first()
    if earthquakes:
        body = {'id': earthquakes.id,
                'location': earthquakes.location,
                'magnitude': earthquakes.magnitude,
                'year':earthquakes.year
                }
        status = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        status = 404

    return make_response(body, status)


@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_by_magnitude(magnitude):
    earthquake_list = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    if earthquake_list:
        quakes = []
        for earth in earthquake_list:
            quake_info = {
                'id': earth.id,
                'location': earth.location,
                'magnitude': earth.magnitude,
                'year': earth.year
            }
            quakes.append(quake_info)
        body = {
            'count': len(earthquake_list),
            'quakes': quakes
        }
        status = 200
    else:
        body = {
            'count': 0,
            'quakes': []
        }
        status = 200  # Return 200 status with an empty list if no earthquakes are found

    return make_response(jsonify(body), status)

    
     

            

if __name__ == '__main__':
    app.run(port=5555, debug=True)
