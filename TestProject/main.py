from flask import Flask, request
from flask_restful import Api, Resource

print(__name__)

application = Flask(__name__)
api = Api(application)

emp_list = [{
    'name': 'Anand', 'age': 31
}]


class Emp(Resource):

    def get(self, name):
        emp = next(filter(lambda x: x['name'] == name, emp_list), None)
        if emp is None:
            return {'message': 'Employee information not found'}
        return {'Employee details': emp}

    def post(self, name):
        emp = next(filter(lambda x: x['name'] == name, emp_list), None)
        print(emp)
        if emp is None:
            employee_info = request.get_json()
            emp_list.append(employee_info)
            return emp_list
        else:
            return {'message': 'Employee information is already present'}


api.add_resource(Emp, '/emp/<string:name>')
application.run(port=8080)
