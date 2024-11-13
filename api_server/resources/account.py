from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import pymysql.cursors
import traceback

parser = reqparse.RequestParser()
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('user_id')

class Account(Resource):

    def db_init(self):
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    def get(self, user_id, id):
        db, cursor = self.db_init()
        sql = "Select * from api.accounts Where user_id = '{}' and id = '{}' and deleted is not True;".format(user_id,id)
        cursor.execute(sql)
        account = cursor.fetchone()
        db.close()
        return jsonify({'data':account})

    def patch(self, user_id, id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance': arg['balance'],
            'account_number': arg['account_number'],
            'user_id': arg['user_id'],
        }
        query = []
        for key, val in account.items():
            if val:
                query.append(key + " = " + "'{}'".format(val))
        query = ", ".join(query)
        sql = """
            UPDATE `api`.`accounts` SET {} WHERE user_id = '{}' and `id` = '{}';
        """.format(query, user_id, id)
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

    def delete(self, user_id, id):
        db, cursor = self.db_init()
        sql = """
            UPDATE `api`.`accounts` SET deleted = True WHERE user_id = '{}' and `id` = '{}'; 
        """.format(user_id,id)
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
    
class Accounts(Resource):

    def db_init(self):
        db = pymysql.connect(host='localhost',
                             user ='root',
                             password='password',
                             database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    def get(self, user_id):
        db, cursor = self.db_init()
        sql = "Select * from api.accounts where user_id = '{}' and deleted is not True".format(user_id)
        cursor.execute(sql)
        accounts = cursor.fetchall()
        db.close()
        print(accounts)
        return jsonify({'data':accounts})

    def post(self, user_id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance': arg['balance'],
            'account_number': arg['account_number'] or 0,
            'user_id': arg['user_id'] or '1900-01-01',
        }
        sql = """
        INSERT INTO `api`.`accounts` (`balance`, `account_number`, `user_id`) VALUES ('{}','{}','{}');
        """.format(account['balance'], account['account_number'], account['user_id'])
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