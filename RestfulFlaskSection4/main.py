import string

from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
api = Api(app)
app.secret_key = "Aani"

jwt = JWT(app, authenticate, identity)  # /auth

items = [{
    "name": "item 1",
    "price": "$10"
}]


class Item(Resource):
    @jwt_required()
    def get(self, name):
        # for item in items:
        #    if item['name'] == name:
        #        return item
        # Using filters for better programming skills
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': 'item already present'}, 400

        requested_data = request.get_json(force=True, silent=True)
        item = {"name": name, 'price': requested_data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item is successfully deleted'}

    def put(self, name):
       # requested_data = request.get_json(force=True, silent=True)
        parser = reqparse.RequestParser()
        parser.add_argument('price',
                            required=True,
                            help='This cannot be left blank')
        requested_data = parser.parse_args()
        if next(filter(lambda x: x['name'] == name, items), None) is None:
            item = {"name": name, 'price': requested_data['price']}
            items.append(item)
        else:
            temp_dict = next(filter(lambda x: x['name'] == name, items), None)
            temp_dict.update(requested_data)
        return {'message': 'items created or updated successfully'}


class Items(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
app.run(port=8080, debug=True)
