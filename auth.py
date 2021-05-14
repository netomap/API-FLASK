import jwt
from variaveis import V
import time

class Auth():

    def __init__(self):
        pass

    def criarToken(self, vetorUsuario):
        id, email, password, nome, idade = vetorUsuario
        agora = round(time.time())
        tempoExpiracao = agora + V().EXPIRES_TOKEN
        payload = {'id': id, 'nome': nome, 'email': email, 'createdAt': agora, 'expiresAt': tempoExpiracao}
        token = jwt.encode(payload=payload, key=V().SECRET_KEY, algorithm='HS256')
        return token

    def verifica(self, token):
        try:
            decoded = jwt.decode(jwt=token, key=V().SECRET_KEY, algorithms=['HS256'])
            agora = round(time.time())
            if (agora >= decoded['expiresAt']):
                return {'success': False, 'message': 'Token expirado'}
            else:
                return {'success': True, 'message': 'ok', 'usuario': decoded}
        except jwt.DecodeError as e:
            return {'success': False, 'message': str(e)}