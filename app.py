#!/usr/bin/env python3
from flask import Flask
from flask_restful import Api

import routes

app = Flask(__name__)
api = Api(catch_all_404s=True)
routes.add_routes_to_resource(api)
api.init_app(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
