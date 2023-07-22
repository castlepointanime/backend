from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from controllers import ContractController
from flask_restful import Api

app = Flask(__name__)
CORS(app)
Swagger(app)
api = Api(app)

api.add_resource(ContractController, '/contract')
    
if __name__ == "__main__":
    app.run(debug=True)