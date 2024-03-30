from pydantic import BaseModel

# Define the data model for a transaction
class TransactionRequest(BaseModel):
    sender: str
    receiver: str
    amount: float

# Define the data model for a balance
class BalanceRequest(BaseModel):
    receiver: str
    amount: float