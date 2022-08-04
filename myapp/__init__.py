from flask import Flask, jsonify, request
from flask_restful import Resource, Api

# from .api.routes import api
# from .site.routes import site

# def create_app():
#     # create the flask app
#     app = Flask(__name__)

#     app.register_blueprint(api)
#     app.register_blueprint(site)

#     return app

# create the flask app
app = Flask(__name__)
# create the API object
api = Api(app)

# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.
class Hello(Resource):
  
    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):
  
        return jsonify({'message': 'hello world'})
  
    # Corresponds to POST request
    def post(self):
          
        data = request.get_json()     # status code
        return jsonify({'data': data}), 201
  
  
# another resource to calculate the square of a number
class Square(Resource):
  
    def get(self, num):
  
        return jsonify({'square': num**2})
  
  
# adding the defined resources along with their corresponding urls
api.add_resource(Hello, '/')
api.add_resource(Square, '/square/<int:num>')

# driver function
if __name__ == '__main__':
  
    app.run(debug = True)