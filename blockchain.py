from time import time
import hashlib

class BlockChain:
    def __init__(self):
        self.chain = []
        self.current_transations = []

    def new_block(self, proof, previous_hash = None):
        block = { # 一个区块的数据结构
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transations,
            "proof": proof,
            "previous_hash": previous_hash or self.hash[self.chain[-1]]
        }

        self.current_transations = []
        self.chain.append[block]
        return block

    def new_transactions(self, sender, recipient, amount) -> int:
        self.current_transations.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })
        return self.last_black['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(blcok, sort_keys = True).encode()
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
