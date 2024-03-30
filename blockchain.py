import datetime
import hashlib
import json
import copy

# Define the Blockchain class
class Blockchain:
    def __init__(self):
        # Initialize the blockchain with an empty chain, difficulty, transactions, balances, and a copy of the chain for peer comparison
        self.chain = []
        self.difficulty = '00000'
        self.transactions = []
        self.balances = dict()
        self.genesis_block()
        self.peer_b = copy.deepcopy(self.chain)
        
    
    def genesis_block(self):
        # Create the genesis block with an empty balances and a previous hash of all zeros
        block = self.create_block(balances=dict(), previous_hash='0'*64)
        self.chain.append(block)


    def create_block(self, balances, previous_hash):
        # Create a new block with a timestamp, nonce, hash, balances, transactions, and previous hash
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),}
        nonce, hash = self.hash(block)
        block['nonce'] = nonce
        block['balances'] = copy.deepcopy(balances)
        block['transactions'] = self.transactions
        block['previous_hash'] = previous_hash
        block['hash'] = hash
        self.transactions = []
        self.balances = dict()
        return block


    def hash(self, block):
        # Calculate the hash and nonce for a given block
        encoded_block = json.dumps(block, sort_keys=True).encode()
        nonce = 0

        while True:
            hash_operation = hashlib.sha256(encoded_block + str(nonce).encode()).hexdigest()

            if hash_operation[:5] == self.difficulty:
                break
            else:
                nonce += 1

        return nonce, hash_operation

    def get_previous_block(self):
        # Get the previous block in the chain
        return self.chain[-1]
    
    def add_transaction(self, sender, receiver, amount):
        # Add a transaction to the list of transactions in the current block
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def add_balance(self, receiver, amount):
        # Add a balance transaction to the current block
        previous_block = self.get_previous_block()
        self.balances[receiver] = amount
        return previous_block['index'] + 1
    

    def is_chain_valid(self):
        # Check if the blockchain is valid by verifying hashes, previous hashes, and difficulty
        previous_block = self.chain[0]
        block_index = 1
 
        while block_index < len(self.chain):
            block = self.chain[block_index]
            if block['previous_hash'] != previous_block['hash']:
                return False
            
            if block['hash'] != self.peer_b[block_index]['hash']:
                return False
 
            if block['hash'][:5] != self.difficulty:
                return False
            previous_block = block
            block_index += 1
 
        return True
