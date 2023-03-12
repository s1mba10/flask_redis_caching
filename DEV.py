import json
import requests
# -----------------------------
from flask import Flask
from flask_caching import Cache
import redis


REDIS_CLIENT = redis.Redis(host='localhost', port=6379, db=0)           # Connect to redis server
cache = Cache()


def get_ip(redis_client=REDIS_CLIENT):
    IP = redis_client.get("IP")
    while not IP:
        try:
            redis_client.set('IP', json.loads(requests.get('https://api.ipify.org?format=json').text)['ip'])
            IP = redis_client.get("IP")
        except:
            continue
    return IP.decode()


def create_app(redis_client=REDIS_CLIENT, IP=get_ip()):
    app = Flask(__name__)
    app.config["CACHE_TYPE"] = "RedisCache"
    cache.init_app(app)

    @app.route("/a")
    @cache.cached(timeout=40)
    def index(redis_client=redis_client, IP=IP):
        return f"<h1>Your current IP is: {IP}</h1>"
    
    app.run(host='127.0.0.1', debug=True)

if __name__ == '__main__':
    create_app()