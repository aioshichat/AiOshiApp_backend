import os
from flask import Flask, Response, json, request

app = Flask(__name__)


@app.route("/oauth2/v2.1/verify", methods=['GET'])
def func001():

    response = Response(response=json.dumps({
        "client_id": os.environ["LINE_CHANNEL_ID"],
        "expires_in":200000,
    }), status=200)
    return response


@app.route("/v2/profile", methods=['GET'])
def func002():

    response = Response(response=json.dumps({
        "userId": "xxxxxx",
    }), status=200)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8001, threaded=True, use_reloader=False)