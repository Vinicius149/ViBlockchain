class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.transacoes = []

    def novo_bloco(self):
        # Cria um novo bloco e o adiciona a chain
        pass

    def nova_transacao(self):
        # Cria uma nova transação e a adiciona na lista de transações
        pass

    @staticmethod
    def hash(bloco):
        # Gera o hash de um bloco
        pass

    @property
    def ultimo_bloco(self):
        # Retorna o último bloco da cadeia
        pass