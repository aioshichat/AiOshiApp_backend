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


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8081, threaded=True, use_reloader=False)