from time import time

class BlockChain:
    def __init__(self):
        self.chain = []
        self.current_transations = []

    def new_block(self, proof, previous_hash = None):
        block = {
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
    def last_black(self):
        pass

    @staticmethod
    def hash(block):
        pass
