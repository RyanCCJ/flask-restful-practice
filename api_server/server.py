from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from flask import Flask
from dotenv import load_dotenv
from flasgger import Swagger
import os

load_dotenv()

template = {
  "swagger": "2.0",
  "info": {
    "title": "Flask Restful API Doc",
    "description": "API description",
    "version": "1.0"
  },
  "host": "localhost",
  "basePath": "",
  "schemes": [
    #"http",
    "https"
  ],
  "tags": [
      {
          "name": "User",
          "description": "系統中的使用者資訊"
      },
      {
          "name": "Account",
          "description": "系統中的帳戶資訊"
      }
  ]
}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_STRING')
db = SQLAlchemy(app)
socketio = SocketIO(app)
swagger = Swagger(app, template=template)