from flask import Flask, request, jsonify, render_template
from flask_restful import Api
from resources.user import Users, User
from resources.account import Accounts, Account
from server import app, socketio, emit
import pymysql
import traceback
import jwt
import time

#app = Flask(__name__)
api = Api(app)
api.add_resource(Users, '/users')
api.add_resource(User, '/user/<id>')
api.add_resource(Accounts, '/user/<user_id>/accounts')
api.add_resource(Account, '/user/<user_id>/account/<id>')

@app.route('/')
def index():
    return "Hello World!"


@app.route('/login')
def login ():
    return render_template('login.html')


@app.route('/FB_login', methods=['POST'])
def FB_login ():
    userID = request.values['userID']
    accessToken = request.values['accessToken']
    print(userID, accessToken)
    return 'success'


@app.errorhandler(Exception)
def handle_error(error):
    status_code = 500
    if type(error).__name__ == "Not Found":
        status_code = 404
    elif type(error).__name__ == "Server Error":
        status_code = 500
    return jsonify({'msg':type(error).__name__}), status_code

# below is for authentication
'''
@app.before_request
def auth():
    token = request.headers.get('auth')
    user_id = request.get_json()['user_id']
    valid_token = jwt.encode({'user_id':user_id, 'timestamp':int(time.time())}, 'password', algorithm='HS256')
    print(valid_token)
    if token != valid_token:
        return {'msg': 'invalid token'}
'''

def get_account(user_id, id):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='password',
                         database='api')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "Select * from api.accounts Where user_id = {} and id = {} and deleted is not True;".format(user_id,id)
    cursor.execute(sql)
    return db, cursor, cursor.fetchone()


@app.route('/user/<user_id>/account/<id>/deposit', methods=['POST'])
def deposit(user_id, id):
    db, cursor, account = get_account(user_id, id)
    money = request.get_json()['money']
    balance = account['balance'] + int(money)
    sql = "UPDATE api.accounts SET balance = {} WHERE id = {} and deleted is not True".format(balance,id)
    response = {}
    try:
        cursor.execute(sql)
        response['msg'] = 'success'
    except:
        traceback.print_exc()
        response['msg'] = 'failed'
    db.commit()
    db.close()
    return jsonify(response)


@app.route('/user/<user_id>/account/<id>/withdraw', methods=['POST'])
def withdraw(user_id, id):
    db, cursor, account = get_account(user_id, id)
    money = request.get_json()['money']
    balance = account['balance'] - int(money)
    response = {}
    if balance < 0:
        response['msg'] = 'money not enough'
        return jsonify(response)
    sql = "UPDATE api.accounts SET balance = {} WHERE id = {} and deleted is not True".format(balance,id)
    try:
        cursor.execute(sql)
        response['msg'] = 'success'
    except:
        traceback.print_exc()
        response['msg'] = 'failed'
    db.commit()
    db.close()
    return jsonify(response)


@app.route('/websocket', methods=['GET'])
def websocket():
    return render_template('websocket.html')


@socketio.on('connect')
def test_connect():
    emit('chatting', {'message':'confirm connection'})


@socketio.on('chatting')
def received(data):
    print('message: ' + data['message'])


@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message',0)
    print(message)
    socketio.emit('chatting', {'message': message})
    return 'success'

 
if __name__ == '__main__':
    #app.debug = True
    #app.run(host='0.0.0.0', port=5000)

    # SSL
    app.run(host='localhost', port=443, ssl_context=('ssl/localhost.crt','ssl/localhost.key'))
