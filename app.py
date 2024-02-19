from flask import Flask
from controllers import router

def create_app():
    app = Flask(__name__)
    app.register_blueprint(router.router)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80, threaded=True, use_reloader=False)