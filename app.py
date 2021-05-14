from flask import Flask, request, make_response, g
from db import UsuarioDAO
from auth import Auth
import time
from variaveis import V

auth = Auth()

app = Flask(__name__)

DESNECESSARIOS = ['/user/login', '/user/signup']

@app.before_request
def middleware():
    endpoint = request.endpoint
    path = request.path
    
    if (path in DESNECESSARIOS):
        print (f'path {path} não precisa do auth')
    else:
        token = request.cookies.get('token')
        resposta = auth.verifica(token)
        if (resposta['success']):
            g.usuario = resposta['usuario']
        else:
            resp = make_response(resposta)
            return resp

@app.route('/user/<id>', methods=['GET'])
def index(id):
    usuarioDAO = UsuarioDAO()
    resposta = usuarioDAO.getUser(id)
    return resposta, 200 if resposta['success'] else 400

@app.route('/user/signup', methods=['POST'])
def signup():
    user = request.form.to_dict()
    usuarioDAO = UsuarioDAO()
    resposta = usuarioDAO.signup(user)
    return resposta, 201 if resposta['success'] else 400

@app.route('/user/<id>', methods=['PUT'])
def editUser(id):
    usuarioDAO = UsuarioDAO()
    user = request.form.to_dict()
    user['id'] = id
    resposta = usuarioDAO.editUser(user)
    return resposta, 200 if (resposta['success']) else 400
    #return Response(resposta, status=200, mimetype='application/json')

@app.route('/user/<id>', methods=['DELETE'])
def deleteUser(id):
    usuarioDAO = UsuarioDAO()
    resposta = usuarioDAO.deleteUser(id)
    return resposta, 202 if (resposta['success']) else 400

@app.route('/user/login', methods=['POST'])
def login():
    usuarioDao = UsuarioDAO()
    user = request.form.to_dict()
    resposta = usuarioDao.login(user)
    if (resposta['success']):
        resp = make_response(resposta)
        resp.set_cookie('token', value=resposta['token'], max_age=V().EXPIRES_COOKIE)
        return resp
    else:
        return resposta, 400

@app.route('/dashboard', methods=['GET'])
def dashboard():
    usuario = g.usuario
    usuario['agora'] = round(time.time())
    return usuario

app.run(debug=True)