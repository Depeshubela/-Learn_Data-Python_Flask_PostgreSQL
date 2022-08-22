from flask import Flask
from flask_script import Manager
from flask_script.commands import ShowUrls    

app = Flask(__name__)

DBScritp = Manager(app)


@DBScritp.command
def init_db():
    print('init database success')


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/register')
def hello():
    return 'hello'

DBScritp.add_command('show', ShowUrls())

if __name__ == '__main__':
    DBScritp.run()
