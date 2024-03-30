# FastAPI Blockchain
A simple blockchain implemented using FastAPI, demonstrating blockchain concepts with easy-to-use API endpoints.

## Overview

This blockchain application provides basic functionality for adding transactions, mining blocks, checking blockchain validity, and exploring the blockchain contents. It is built on top of FastAPI, a modern Python web framework known for its high performance and intuitive API design.

## Features

- **Adding Transactions**: Users can add transactions to the blockchain by specifying sender, receiver, and amount.
- **Mining Blocks**: Blocks can be mined to add transactions to the blockchain and maintain its integrity.
- **Checking Blockchain Validity**: Endpoint to validate the integrity of the blockchain.
- **Exploring the Blockchain**: View the entire blockchain to observe block contents and transaction history.

## Usage

Follow these steps to explore and interact with the FastAPI-based blockchain:

### Launch the FastAPI Blockchain Application

Open your terminal and run the following command to start the FastAPI application:

```bash
uvicorn main:app --reload
