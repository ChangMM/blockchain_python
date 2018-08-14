from time import time
import hashlib
import json
from flask import Flask, jsonify, request
from uuid import uuid4
from urllib.parse import urlparse

class BlockChain:
    def __init__(self):
        self.chain = []
        self.current_transations = []
        self.nodes = set()
        self.new_block(100, previous_hash = 1) # first blockchain

    def register_node(self, address:self):
        parsed_url = rlparse(address)
        self.nodes.add(parsed_url.netloc)

    def new_block(self, proof=0, previous_hash = None):
        block = { # 一个区块的数据结构
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transations,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.last_block)
        }
        self.current_transations = []
        self.chain.append(block)
        return block

    def new_transactions(self, sender="", recipient="", amount=0) -> int:
        self.current_transations.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof) -> int:
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof = proof + 1
        return proof

    def valid_proof(self, last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[0:4] == "0000"

app = Flask(__name__)
blockchain = BlockChain()
node_identifier = str(uuid4()).replace("-", "")

@app.route("/transactions/new", methods=["POST"])
def transactions_new():
    values = request.get_json()
    required = ["sender", "recipient", "amount"]
    if not all(k in values for k in required) or values is None:
        return "missing params", 400
    index = blockchain.new_transactions(sender=values["sender"], recipient=values["recipient"], amount=values["amount"])
    response = {
        "message": f"new transactions will be added to {index}",
        "index": index
    }
    return jsonify(response), 201

@app.route("/mine", methods=["GET"])
def mine():
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block["proof"],)
    blockchain.new_transactions(sender="0", recipient=node_identifier, amount=5)
    block = blockchain.new_block(proof=proof)
    response = {
        "message": "New Block added",
        "data":{
            "index":block["index"],
            "transactions": block["transactions"],
            "proof": block["proof"],
            "timestamp": block["timestamp"],
            "previous_hash": block["previous_hash"]
        }
    }
    return jsonify(response), 200

@app.route("/chain", methods=["GET"])
def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route("/node/register", methods=["POST"])
def register_node():
    values = request.get_json()
    node = values.get("nodes")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
