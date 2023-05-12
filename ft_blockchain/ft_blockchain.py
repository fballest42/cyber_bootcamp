import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.new_trasaction = []
        self.nodes = set()
        self.end_hash = "4242"
        self.new_block(old_hash = 1, proof = 100)
    
    def new_block(self, proof, old_hash = None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transaction': self.new_trasaction,
            'proof': proof,
            'previous hash': old_hash}
        self.new_trasaction = []
        self.chain.append(block)
        return block

    def transaction(self, sender, recipient, amount):
        self.new_transaction.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount})
        return self.last_block['index'] + 1
    
