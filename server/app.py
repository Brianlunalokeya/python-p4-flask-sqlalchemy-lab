from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get(id)
    if animal:
        response_body = f'''
            <h1>{animal.name}</h1>
            <h2>Species: {animal.species}</h2>
            <h3>Zookeeper: {animal.zookeeper.name}</h3>
            <h3>Enclosure: {animal.enclosure.environment}</h3>
        '''
        status_code = 200
    else:
        response_body = '<h1>Animal not found</h1>'
        status_code = 404

    headers = {}
    return make_response(response_body, status_code, headers)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get(id)
    if zookeeper:
        animals = zookeeper.animals
        response_body = f'''
            <h1>{zookeeper.name}</h1>
            <h2>Birthday: {zookeeper.birthday}</h2>
            <h3>Animals:</h3>
            <ul>
        '''
        for animal in animals:
            response_body += f'<li>{animal.name} - {animal.species}</li>'
        response_body += '</ul>'
        status_code = 200
    else:
        response_body = '<h1>Zookeeper not found</h1>'
        status_code = 404

    headers = {}
    return make_response(response_body, status_code, headers)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get(id)
    if enclosure:
        animals = enclosure.animals
        response_body = f'''
            <h1>Enclosure: {enclosure.environment}</h1>
            <h2>Open to Visitors: {enclosure.open_to_visitors}</h2>
            <h3>Animals:</h3>
            <ul>
        '''
        for animal in animals:
            response_body += f'<li>{animal.name} - {animal.species}</li>'
        response_body += '</ul>'
        status_code = 200
    else:
        response_body = '<h1>Enclosure not found</h1>'
        status_code = 404

    headers = {}
    return make_response(response_body, status_code, headers)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
