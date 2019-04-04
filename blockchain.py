from time import time
import datetime
import hashlib as hasher
import acoustic.acoustid_check as ac

""" Class for transactions made on the blockchain. Each transaction has a
    sender, recipient, and value.
    """
class Transaction:
    
    """ Transaction initializer """
    def __init__(self, author, genre, media):
        self.author = author
        self.genre = genre
        self.media = media
        f = open(media, "rb")
        content = f.readlines()
        self.hash_media = hasher.sha256(content).hexdigest()
    
    """ Converts the transaction to a dictionary """
    def toDict(self):
        return {
            'author': self.author,
            'genre': self.genre,
            'media': self.media,
            "hash_media" : self.hash_media
    }

    def __str__(self):
        toString = self.author + " : " + self.genre + " (" + self.media + ") "
        return toString;

""" Class for Blocks. A block is an object that contains transaction information
    on the blockchain.
    """
class Block:
    def __init__(self, index, transaction, previous_hash):
        #TODO: Block initializer
        
        self.index = index
        self.timestamp = time()
        self.previous_hash = previous_hash
        self.transaction = transaction
        self.time_string = timestamp_to_string();
    
    def compute_hash(self):
        #TODO Implement hashing
        concat_str = str(self.index) + str(self.timestamp) + self.previous_hash + self.transaction['author'] + self.transaction['genre'] + self.transaction['hash_media']
        hash_result = hasher.sha256(concat_str).hexdigest()
        return hash_result
    
    """ Function to convert a timestamp to a string"""
    def timestamp_to_string():
        return datetime.datetime.fromtimestamp(self.timestamp).strftime('%H:%M')
    
    def __str__(self):
        toString =  str(self.index) + "\t" + str(self.timestamp) +"\t\t" + str(self.previous_hash) + "\n"
        for tx in self.data:
            toString +=  "\t" + str(tx) + "\n"
        return toString;

""" Blockchain class. The blockchain is the network of blocks containing all the
    transaction data of the system.
    """
class Blockchain:
    def __init__(self):
        #TODO: implement Blockchain class initializer
        
        
        self.unconfirmed_transactions = {}
        self.chain = []
    
    def create_genesis_block(self):
        #TODO: implement creating a new genesis block
        empty_media = {
        "media" : "",
        "genre": "",
        "author": ""
        }
        new_block = Block(index=0, media=empty_media, previous_hash=0)
        self.add_block(new_block)
        return new_block;
    
    def new_transaction(self, author, genre, media):
        #TODO: implement adding new transactions
        new_trans = Transaction(author, genre, media).toDict();
        self.unconfirmed_transactions= new_trans.copy()

        return new_trans;
    
    def mine(self):
        #TODO: create a block, verify its originality and add to the blockchain
        if (len(self.chain) ==0):
            block_idx = 1
            previous_hash = 0
        else:
            block_idx = self.chain[-1].index + 1
            previous_hash = self.chain[-1].compute_hash
        block = Block(block_idx, unconfirmed_transactions, previous_hash);
        if(self.verify_block(block)):
            self.add_block(block)
        return block
    
    def verify_block(self, block):
        #TODO: verify song originality and previous hash
        #check previous hash
        if len(self.chain) ==0:
            previous_hash = 0;
        else:
            previous_hash = self.chain[-1].compute_hash()
        if block.previous_hash == previous_hash:
            return 1
        else:
            return 0
        #check originality
        for prev_block in self.chain[1:]:
            if block.transaction['genre'] == prev_block.transaction['genre']:
                if block.transaction['genre'] == 'music':
                    score = ac.calc_accuracy(block.transaction['media'], prev_block.transacton['media'])  

        return 1;
    
    def add_block(self, block):
        #TODO: add the block to chain
        
        self.chain.append(block);
    
    def check_integrity(self):
        #TODO implement blockchain integrity check
        
        return 0

    """ Function that returns the last block on the chain"""
    @property
    def last_block(self):
        return self.chain[-1]
