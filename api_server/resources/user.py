from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from server import db
from models import UserModel
import pymysql
import pymysql.cursors
import traceback

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

class User(Resource):

    def db_init(self):
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    def get(self, id):
        db, cursor = self.db_init()
        sql = "Select * from api.users Where id = '{}' and deleted is not True;".format(id)
        cursor.execute(sql)
        user = cursor.fetchone()
        db.close()
        return jsonify({'data':user})

    def patch(self, id):
        # original code
        '''
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'],
            'birth': arg['birth'],
            'note': arg['note'],
        }
        query = []
        for key, val in user.items():
            if val:
                query.append(key + " = " + "'{}'".format(val))
        query = ", ".join(query)
        sql = """
            UPDATE `api`.`users` SET {} WHERE (`id` = '{}');
        """.format(query, id)
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
        '''

        # below is for SQL ORM
        arg = parser.parse_args()
        user = UserModel.query.filter_by(id=id, deleted=False).first()
        if arg['name']: user.name = arg['name']
        response = {}
        try:
            db.session.commit()
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        return jsonify(response)


    def delete(self, id):
        # original code
        '''
        db, cursor = self.db_init()
        sql = """
            UPDATE `api`.`users` SET deleted = True WHERE (`id` = '{}'); 
        """.format(id)
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
        '''

        # below is for SQL ORM
        user = UserModel.query.filter_by(id=id, deleted=False).first()
        response = {}
        try:
            db.session.delete(user)
            db.session.commit()
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        return jsonify(response)
    
    
class Users(Resource):

    def db_init(self):
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    def get(self):
        # original code
        '''
        db, cursor = self.db_init()
        arg = parser.parse_args()
        sql = 'Select * from api.users where deleted is not True'
        if arg['name']:   sql += " and name = '{}'".format(arg['name'])
        if arg['gender']: sql += " and gender = '{}'".format(arg['gender'])
        if arg['birth']:  sql += " and birth = '{}'".format(arg['birth'])
        if arg['note']:   sql += " and note = '{}'".format(arg['note'])
        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        print(users)
        return jsonify({'data':users})
        '''

        # below is for SQL ORM
        users = UserModel.query.filter(UserModel.deleted.isnot(True)).all()
        return jsonify({'data': list(map(lambda user: user.serialize(), users))})

    def post(self):
        # original code
        '''
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'] or 0,
            'birth': arg['birth'] or '1900-01-01',
            'note': arg['note'],
        }
        sql = """
        INSERT INTO `api`.`users` (`name`, `gender`, `birth`, `note`) VALUES ('{}','{}','{}','{}');
        """.format(user['name'], user['gender'], user['birth'], user['note'])
        response = {}
        status_code = 200
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = 'failed'
        db.commit()
        db.close()
        return make_response(jsonify(response), status_code)
        '''

        # below is for SQL ORM
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'] or 0,
            'birth': arg['birth'] or '1900-01-01',
            'note': arg['note'],
        }
        response = {}
        status_code = 200
        try:
            new_user = UserModel(name=user['name'], 
                             gender=user['gender'], 
                             birth=user['birth'],
                             note=user['note'])
            db.session.add(new_user)
            db.session.commit()
            response['msg'] = 'success'
        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = 'failed'
        return make_response(jsonify(response), status_code)
        