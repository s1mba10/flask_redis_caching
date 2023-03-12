import json
# -----------------------------
import requests
from flask import Flask
from flask_caching import Cache


def get_ip():
    IP = 0
    while not IP:
        try:
            IP = json.loads(requests.get('https://api.ipify.org?format=json').text)['ip']   
        except:
            continue
    return IP


def create_app(IP=get_ip()):

    cache = Cache()
    app = Flask(__name__)
    app.config["CACHE_TYPE"] = "RedisCache"
    cache.init_app(app)

    @app.route("/")
    @cache.cached(timeout=30)
    def index(IP=IP):
        return f"<h1>Your current IP is: {IP}</h1>"
    
    app.run(host='127.0.0.1', debug=True)

if __name__ == '__main__':
    create_app()
