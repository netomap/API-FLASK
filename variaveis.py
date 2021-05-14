class V:

    def __init__(self):
        self.SECRET_KEY = 'aa6c3b5781c63657510ff1593e8a9b3310b1248b7010fe5d4cd2f2870d3d4894'
        self.EXPIRES_TOKEN = 60 # segundos
        self.EXPIRES_COOKIE = 60 # segundos
    
    def gerarChaveAleatoria(self):   # só é chamado apenas uma vez
        import time
        import hashlib
        return hashlib.sha256(bytearray(str(time.time()), encoding='utf-8')).hexdigest()