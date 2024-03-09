from flask import Flask
from controllers import router_liff
from models.database import init_db
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    # CORS(
    #     app,
    #     supports_credentials=True
    # )
    # CORS(app, origins=["*"], methods=["POST"])

    app.config.from_object('models.config.Config')
    init_db(app)

    app.register_blueprint(router_liff.router)

    return app

app = create_app()


@app.after_request
def after_request(response):
    del response.headers['Access-Control-Allow-Origin']
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    # response.headers.add('Access-Control-Allow-Headers', 'Authorization')
    # response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    # response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8081, threaded=True, use_reloader=False)