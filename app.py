from flask import Flask
from controllers import router
from models.database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object('models.config.Config')
    init_db(app)

    app.register_blueprint(router.router)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80, threaded=True, use_reloader=False)