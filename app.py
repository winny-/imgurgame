from flask import Flask, render_template, request
import imgur_game


app = Flask(__name__)

@app.route('/')
def game():
    s = request.args.get('s', '')
    if len(s) == 5:
        urls = imgur_game.imgur_game2(s)
    else:
        urls = []
    return render_template('imgur.html', urls=urls, s=s)


if __name__ == '__main__':
    app.debug = True
    app.run()