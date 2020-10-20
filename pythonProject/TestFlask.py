from flask import Flask, jsonify, request ,render_template

stores = [
    {
        'store_name': 'Rancho bernardo',
        'item_list': [{'name': 'item1', 'price': '$10'}]
    }
]

api = Flask(__name__)


@api.route('/')
def func():
    return render_template('index.html')


@api.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json();
    new_store = {'store_name': request_data['name'],
                 'item_list': []}
    stores.append(new_store)
    return jsonify(new_store)


@api.route('/store', methods=['GET'])
def get_store_list():
    return jsonify({'store_list': stores})


@api.route('/store/<string:name>')  # http://127.0.0.1:8080/getStore/RanchoBernardo
def get_store(name):
    for store in stores:
        if store['store_name'] == name:
            return jsonify(store)
    return "store not found in the list"


@api.route('/store/<string:name>/<string:item>', methods=['POST'])
def create_item_in_store(name, item):
    request_data = request.get_json()
    for store in stores:
        if store['store_name'] == name:
            store['item_list'].append(request_data)
            return 'received item successfully'
    return 'store not found'

@api.route('/store/<string:name>/<string:item>')  # http://127.0.0.1:8080/getItemInStore/RanchoBernardo/item123
def get_item_in_store(name, item):
    for store in stores:
        if store['store_name'] == name:
            item_list = store['item_list']
            for sku in item_list:
                if sku['name'] == item:
                    return jsonify(sku)
                else:
                    return jsonify({'message': 'item not found'})


api.run(port=8080)
