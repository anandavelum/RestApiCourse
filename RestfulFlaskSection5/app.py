import string

from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from db import db
from user import User
import sqlite3

app = Flask(__name__)
api = Api(app)
app.secret_key = "Aani"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWT(app, authenticate, identity)  # /auth


@app.before_first_request
def create_tables():
    db.create_all()
    try:
        user = User(3, "Nakshathra", "Nakshathra")
        user.save_to_db()
        user = User(4, "Murugan", "Murugan")
        user.save_to_db()
    except:
        print('User already present')


class Item(Resource):
    @classmethod
    def get_Item_By_Name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        rs = cursor.execute('select * from items where item_name =?', (name,))
        row = rs.fetchone()
        connection.close()
        print(row)
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        else:
            return None

    @classmethod
    def insert_item(cls, item_vals):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        cursor.execute('INSERT INTO ITEMS VALUES(?,?)', item_vals)
        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):
        item = Item.get_Item_By_Name(name)
        if item:
            return item
        return {'message': 'item not present in database'}, 404

    def post(self, name):
        item = Item.get_Item_By_Name(name)
        if item:
            return {'message': 'item already present in database'}, 400
        requested_data = request.get_json(force=True, silent=True)
        item_vals = (name, requested_data['price'])
        Item.insert_item(item_vals)
        return_string = f"{name} with {requested_data['price']} is successfully inserted into table"
        return {'message': return_string}, 201

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM ITEMS WHERE item_name = ?', (name,))
        connection.commit()
        connection.close()
        return_string = f"{name} is successfully deleted from table"
        return {'message': return_string}

    def put(self, name):
        # requested_data = request.get_json(force=True, silent=True)
        parser = reqparse.RequestParser()
        parser.add_argument('price',
                            required=True,
                            help='This cannot be left blank')
        requested_data = parser.parse_args()
        item = Item.get_Item_By_Name(name)
        item_vals = (name, requested_data['price'])
        if item:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute('update items set price = ? where item_name =?', (requested_data['price'], name))
            connection.commit()
            connection.close()
            return_string = f"{name} is successfully updated in the table"
            return {'message': return_string}
        else:
            Item.insert_item(item_vals)
            return_string = f"{name} with {requested_data['price']} is successfully inserted into table"
            return {'message': return_string}, 201

        return {'message': 'items created or updated successfully'}


class Items(Resource):
    def get(self):
        items = []
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        rs = cursor.execute('select * from items')
        rows = rs.fetchall()
        connection.close()
        print(rows)
        if rows:
            for row in rows:
                items.append({'name': row[0], 'price': row[1]})
            return {'items': items}
        else:
            return {'message': 'Table is empty'}


if __name__ == '__main__':
    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(Items, '/items')
    db.init_app(app)
    app.run(port=8080, debug=True)
