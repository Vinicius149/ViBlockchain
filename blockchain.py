import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.transacoes = []

        # Cria o bloco gênese (inicial)
        self.novo_bloco(hash_anterior=1, prova=100)

    def prova_de_trabalho(self, ultima_prova):
        # Algoritmo simples de prova de trabalho:
        # - Encontre um número p' tal que hash(pp') contenha 4 zeros à esquerda, onde p é o último p'
        # - p é a última prova, e p' é a nova prova
        prova = 0
        while self.validar_prova(ultima_prova, prova) is False:
            prova += 1

        return prova
    
    @staticmethod
    def validar_prova(ultima_prova, prova):
        # Valida a prova: Será que hash(ultima_prova, prova) contém 4 zeros à esquerda?
        tentativa = f'{ultima_prova}{prova}'.encode()
        tentativa_hash = hashlib.sha256(tentativa).hexdigest()
        return tentativa_hash[:4] == "0000"
    

    def novo_bloco(self, prova, hash_anterior=None):
        # Cria um novo bloco e o adiciona a chain
        bloco = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transacoes': self.transacoes,
            'prova': prova,
            'hash_anterior': hash_anterior or self.hash(self.chain[-1]),
        }

        # Reseta a lista de transações
        self.transacoes = []

        self.chain.append(bloco)
        return bloco

    def nova_transacao(self, remetente, destinataio, valor):
        # Cria uma nova transação e a adiciona na lista de transações
        self.transacoes.append({
            'remetente': remetente,
            'destinatario': destinataio,
            'valor': valor
        })

        return self.ultimo_bloco['index'] + 1

    @staticmethod
    def hash(bloco):
        # Cria um hash SHA-256 do bloco
        bloco_string = json.dumps(bloco, sort_keys=True).encode()
        return hashlib.sha256(bloco_string).hexdigest()

    @property
    def ultimo_bloco(self):
        # Retorna o último bloco da cadeia
        pass


app = Flask(__name__)

node_id = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route('/minerar', methods=['GET'])
def minerar():
    return 'Mineração iniciada!'

@app.route('/transacao/nova', methods=['POST'])
def nova_transacao():
    return "Transação adicionada com sucesso!"

@app.route('/chain', methods=['GET'])
def obter_cadeia():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
