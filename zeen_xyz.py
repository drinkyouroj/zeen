from flask import Flask, render_template
from flask.ext.script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
    return '<h1>This is zeen.xyz</h1>'

@app.route('/user/<name>')
def user(name):
    return "greetings %s" % name

if __name__ == '__main__':
    manager.run()
