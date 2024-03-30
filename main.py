from fastapi import FastAPI, HTTPException
import uvicorn
import copy
import random
from blockchain import Blockchain
from schemas import TransactionRequest, BalanceRequest


app = FastAPI()
blockchain = Blockchain()

# Endpoint to simulate hacking a block
@app.get('/hack_block')
def hack_block():
    random_block_id = random.randint(1, len(blockchain.chain)-1)
    block = blockchain.chain[random_block_id]
    nonce, hash = blockchain.hash(block)
    block['hash'] = hash
    blockchain.chain[random_block_id] = block
    response = {'message': 'A block is HACKED',
            'index': block['index'],
            'timestamp': block['timestamp'],
            'nonce': block['nonce'],
            'previous_hash': block['previous_hash'],
            'hash': block['hash'],
            'balances': block['balances'],
            'transactions': block['transactions']}
    return response

# Endpoint to check if the blockchain is valid
@app.get('/valid')
def valid():
    if blockchain.is_chain_valid():
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return response

# Endpoint to mine a new block
@app.get('/mine_block')
def mine_block():
    # Check if the blockchain is valid before mining a new block
    if not blockchain.is_chain_valid():
        raise HTTPException(status_code=400, detail="Blockchain is not valid")

    # Get the previous block to determine the previous hash
    previous_block = blockchain.get_previous_block()
    previous_hash = previous_block['hash']

    # Aggregate balances from the previous block and the current block
    balances = {k: blockchain.balances.get(k, 0) + previous_block['balances'].get(k, 0) for k in set(blockchain.balances) | set(previous_block['balances'])}

    # Create a new block with the aggregated balances and previous hash
    block = blockchain.create_block(balances, previous_hash)

    is_block_valid = True
    sender_aggregations = {}
    receiver_aggregations = {}
    for transaction in block['transactions']:
        sender = transaction["sender"]
        receiver = transaction["receiver"]
        amount = transaction["amount"]
        
        if sender in sender_aggregations:
            sender_aggregations[sender] += amount
        else:
            sender_aggregations[sender] = amount

        if receiver in receiver_aggregations:
            receiver_aggregations[receiver] += amount
        else:
            receiver_aggregations[receiver] = amount

    if not block['balances'] and sender_aggregations:
        is_block_valid = False
        raise HTTPException(status_code=400, detail="Invalid transaction data: Not enough amount")
    
    if block['balances']:
        for sender in sender_aggregations:
            sender_balance = block['balances'].get(sender, 0)
            if sender_balance < sender_aggregations[sender]:
                is_block_valid = False
                raise HTTPException(status_code=400, detail=f"Invalid transaction data for {sender}: Not enough amount")
            else:
                block['balances'][sender] = sender_balance - sender_aggregations[sender]

        for receiver in receiver_aggregations:
            receiver_balance = block['balances'].get(receiver, 0)
            block['balances'][receiver] = receiver_balance + receiver_aggregations[receiver]

    if is_block_valid:
        # Append the mined block to the blockchain and update the peer copy
        blockchain.chain.append(block)
        blockchain.peer_b = copy.deepcopy(blockchain.chain)

    response = {'message': 'A block is MINED',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'nonce': block['nonce'],
                'previous_hash': block['previous_hash'],
                'hash': block['hash'],
                'balances': block['balances'],
                'transactions': block['transactions']}

    return response

# Endpoint to get the current state of the blockchain
@app.get('/get_chain')
def display_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return response


# Endpoint to add a new transaction to the blockchain
@app.post('/add_transaction')
def add_transaction(transaction_data: TransactionRequest):
    data = transaction_data.dict()
    if 'sender' not in data or 'receiver' not in data or 'amount' not in data:
        raise HTTPException(status_code=400, detail="Invalid transaction data")
    
    if data['sender'] == data['receiver']:
        raise HTTPException(status_code=400, detail="Sender cannot be the same with receiver")

    if data['amount'] <= 0:
        raise HTTPException(status_code=400, detail="Transaction amount must be greater than zero")

    # Add the transaction to the current list of transactions in order to be included in the next mined block 
    index = blockchain.add_transaction(data['sender'], data['receiver'], data['amount'])
    response = {'message': f'Transaction added to block {index}'}
    return response

# Endpoint to add a new balance to the blockchain
@app.post('/add_balance')
def add_balance(balance_data: BalanceRequest):
    data = balance_data.dict()
    if 'receiver' not in data or 'amount' not in data:
        raise HTTPException(status_code=400, detail="Invalid transaction data")

    if data['amount'] <= 0:
        raise HTTPException(status_code=400, detail="Balance must be greater than zero")
    
    # Add the balances to the current list of balances in order to be included in the next mined block
    index = blockchain.add_balance(data['receiver'], data['amount'])
    response = {'message': f'Balance added to block {index}'}
    return response


# Run the FastAPI app using uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
