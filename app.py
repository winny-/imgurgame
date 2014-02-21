from flask import Flask, render_template, request
import imgur_game
from store import redis, redis_url
import sys
from time import time


TTL = 60 * 60 * 24
app = Flask(__name__)


@app.route('/')
def game():
    s = request.args.get('s', '')
    canonical_s = s.lower()
    log('Redis url {}'.format(redis_url))
    log('Processing {} canonical {}'.format(s, canonical_s))
    if len(s) == 5:
        url_s = redis.get(canonical_s)
        log('Passed length check. Redis reports {}.'.format(url_s))
        if not url_s:
            log('Fetching images, not found in cache.')
            urls = list(imgur_game.imgur_game_api(s))
            log('Fetched urls {} in list'.format(len(urls)))
            redis.setex(canonical_s, urls, TTL)
            log('Saved to Redis')
        else:
            log('Found in cache.')
            urls = eval(url_s)
    else:
        urls = []
    log('Rendering template imgur.html')
    return render_template('imgur.html', urls=urls, s=s)


def log(message):
    print(str(time())+' '+message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.debug = True
    app.run()
