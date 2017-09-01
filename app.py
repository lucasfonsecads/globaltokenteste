from flask import Flask
from flask import Flask, render_template, request, abort, session, redirect, jsonify
# from firebase_token_generator import create_token #Firebase desactivate
import sendgrid
import json
import os
import string
from sendgrid.helpers.mail import *
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
import os
import  binascii


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///solidareasy.sqlite3' #access bd in SQLAlchemy
app.config['SECRET_KEY'] = 'random string'

db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    token = db.Column(db.String(120), unique=True)

    def __init__(self, name, email, token):
        self.name = name
        self.email = email
        self.token = token


app = Flask(__name__, static_folder='public', static_url_path='')

@app.route('/check', methods = ['POST'])
def token():
    tok = binascii.hexlify(os.urandom(16))
    return tok

@app.route('/teste', methods = ['POST'])
def tokenteste():
	teste = token()
	data = { "token: "
	[{
		"tokens: " +  teste
	}]}
	return data

# def tokenC(): #Firebase token desactivate
# 	auth_payload = {"uid": "1", "auth_data": "foo", "other_auth_data": "bar"} # token generator with firebase
# 	options = {"admin": True}
# 	token = create_token("<AIzaSyARXSs-bBjRg4FGya6yV7opSEaHibywSj0>", auth_payload, options)
# 	return token
# 	return "<a href=" + token +">Clique Aqui</a>"
	
@app.route('/token/check', methods= ['POST', 'GET']) #Route to give all token query 
def tokenverif():
	dev = users.query.get(id)
	dev.token = request.json.get('token', dev.token)
	# token()
	# user = users(token())
	# db.session.add(user)
	# db.session.commit()
	# return ("WORK GOOD")

@app.route('/add/token-user', methods = ['POST'])  #TEST FROM ADD NEW TOKEN AND USER TO BD
def create_tok():
	if not reques.json or not'name' in request.json:
		abort(400)
	user = users(request.json.name, request.json.get('email', ''), request.json.get('token', + token()))
	db.session.add(user)
	db.session.commit()
	return jsonify({'users': user}), 201


@app.route('/', methods=['POST'])
def sendMail():
	token()
	sg = sendgrid.SendGridAPIClient(apikey='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')
	data = {
	"personalizations": [
	    {
	      "to": [
	        {
	          "email": "lucasfonmiranda@gmail.com"
	        }
	      ],
	      "subject": "O link do seu video esta aqui"
	    }
	  ],
	  "from": {
	    "email": "contato@solidareasy.com"
	  },
	  "content": [
	    {
	      "type": "text/html",
	      "value": ("Acesse seu video aqui: " + token()) 
	    }
	  ]
	}
	response = sg.client.mail.send.post(request_body=data)
	return jsonify({"status": response.status_code})


if __name__ == "__main__":
	db.create_all()
	app.secret_key = os.urandom(12)
	app.run(debug=True, host='0.0.0.0', port=4000)