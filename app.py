from flask import Flask, redirect
from flasgger import Swagger
from api.route.nfe import nfe_api


def create_app():
    my_app = Flask(__name__)

    my_app.config['SWAGGER'] = {
        'title': 'NFE Validate API',
    }
    Swagger(my_app)
    my_app.register_blueprint(nfe_api, url_prefix='/api')

    return my_app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
