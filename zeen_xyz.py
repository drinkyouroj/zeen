from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'This is zeen.xyz'

if __name__ == '__main__':
    app.run( debug=True )