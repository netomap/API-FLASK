from typing import final
from weakref import finalize
import mysql.connector
from mysql.connector import Error
from variaveis import V
from auth import Auth
from db_variables import Var

class UsuarioDAO:

    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user=Var().DB_USER,
                password=Var().DB_PASSWORD,
                port=Var().DB_PORT,
                database=Var().DB_NAME
            )
        except Error as e:
            print (e)
            return False
    
    def signup(self, user):
        if (self.conn.is_connected()):
            try:
                cursor = self.conn.cursor()
                cursor.execute('INSERT INTO users (email, password, nome, idade) VALUES ("{}","{}","{}","{}");'.format(
                    user['email'], user['password'], user['nome'], user['idade']
                ))
                self.conn.commit()
                success, message = True, 'Usuário inserido com sucesso!'

            except Error as e:
                if (e.msg.find('Duplicate entry', 0) != -1):
                    success, message = False, 'email já cadastrado no banco'
                else:
                    success, message = False, str(e)

        else:
            success, message = False, 'sem conexão com db'
        
        cursor.close()
        self.conn.close()
        return {'success': success, 'message': message}
    
    def getUser(self, id):
        usuario = None
        if (self.conn.is_connected()):
            cursor = self.conn.cursor()
            try:
                cursor.execute('SELECT * FROM users WHERE id="{}";'.format(id))
                ut = cursor.fetchall() # usertupla. 
                if (len(ut) == 1):
                    ut = ut[0] # o índice zero é porque retorna um vetor
                    usuario = {'id': ut[0], 'email': ut[1], 'nome': ut[3], 'idade': ut[4]}
                    success, message = True, 'usuário encontrado.'
                else:
                    success, message = False, 'usuário não encontrado.'
            except Error as e:
                success, message = False, str(e)

        else:
            success, message = False, 'sem conexão com db'
        
        cursor.close()
        self.conn.close()
        return {'success': success, 'message': message, 'usuario': usuario}
    
    def editUser(self, user):
        if (self.conn.is_connected()):
            cursor = self.conn.cursor()
            try:
                cursor.execute('UPDATE users SET nome="{}", idade="{}" WHERE id="{}";'.format(
                    user['nome'], user['idade'], user['id']
                ))
                self.conn.commit()
                if (cursor.rowcount == 1):
                    success, message = True, 'usuário editado com sucesso'
                else:
                    success, message = False, 'credenciais não encontradas'
            except Error as e:
                success, message = False, str(e)

        else:
            success, message = False, 'sem conexão com db'

        cursor.close()
        self.conn.close()
        return {'success': success, 'message': message}
    
    def deleteUser(self, id):
        if (self.conn.is_connected()):
            cursor = self.conn.cursor()
            try:
                cursor.execute('DELETE FROM users WHERE id="{}"'.format(id))
                self.conn.commit()
                if (cursor.rowcount == 1):
                    success, message = True, 'usuário excluído'
                else:
                    success, message = False, 'usuário não encontrado'
            except Error as e:
                success, message = False, str(e)
        else:
            success, message = False, 'sem conexão com db'

        cursor.close()
        self.conn.close()
        return {'success': success, 'message': message}
    
    def login(self, user):
        if (self.conn.is_connected()):
            cursor = self.conn.cursor()
            token = None
            try:
                cursor.execute('SELECT * FROM users WHERE email="{}" AND password="{}"'.format(
                    user['email'], user['password']
                ))
                resultado = cursor.fetchall()
                if (len(resultado) == 1):
                    token = Auth().criarToken(resultado[0])
                    success, message = True, 'usuário logado'
                else:
                   success, message = False, 'credenciais inválidas'
            except Error as e:
                success, message = False, str(e)

        else:
            success, message = False, 'sem conexão com db'
        
        cursor.close()
        self.conn.close()
        return {'success': success, 'message': message, 'token': token}