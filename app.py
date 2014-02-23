from flask import Flask, render_template, request, redirect, url_for
from imgur_game import game_http
from store import redis
import sys
from time import time
from pickle import loads, dumps
from random import randrange


TTL = 60 * 60 * 24
app = Flask(__name__)


@app.route('/')
def game():
    start_time = time()
    s = request.args.get('s', '')
    canonical_s = s.lower()

    log('Processing {} canonical {}'.format(s, canonical_s))
    if len(s) == 5:
        cached_images = redis.get(canonical_s)
        log('Passed length check.')
        if not cached_images:
            log('Fetching images, not found in cache.')
            images = list(game_http(s))
            log('Fetched images {} in list'.format(len(images)))
            redis.setex(canonical_s, dumps(images), TTL)
            log('Saved to Redis')
        else:
            log('Found in cache.')
            images = loads(cached_images)
    else:
        images = []

    log('Rendering template imgur.html')
    end_time = time() - start_time
    return render_template('imgur.html', images=images, s=s, time=end_time)

@app.route('/random')
def random_game():
    a, z = ord('a'), ord('z')
    s = ''.join(chr(randrange(a, z+1)) for _ in range(5))
    return redirect(url_for('game', s=s))


def log(message):
    print(str(time())+' '+message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.debug = True
    app.run()
