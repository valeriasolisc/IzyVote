import hashlib
import json
import os
from datetime import datetime
from typing import List, Dict, Any

class Block:
    """Individual block in the blockchain"""
    
    def __init__(self, index: int, votes: List[Dict], previous_hash: str):
        self.index = index
        self.timestamp = datetime.utcnow().isoformat()
        self.votes = votes  # List of anonymous votes
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate hash for this block"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "votes": self.votes,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 4):
        """Mine block with proof of work"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary for JSON serialization"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "votes": self.votes,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }

class VotingBlockchain:
    """Blockchain implementation for voting system"""
    
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_votes: List[Dict] = []
        self.blockchain_file = "instance/blockchain.json"
        self.load_blockchain()
        if not self.chain:
            self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(0, [], "0")
        genesis_block.mine_block()
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_vote(self, election_id: int, option: str):
        """Add a vote to pending votes"""
        vote = {
            "election_id": election_id,
            "option": option,
            "timestamp": datetime.utcnow().isoformat(),
            "vote_id": hashlib.sha256(f"{election_id}{option}{datetime.utcnow()}".encode()).hexdigest()[:16]
        }
        self.pending_votes.append(vote)
    
    def mine_pending_votes(self):
        """Mine all pending votes into a new block"""
        if not self.pending_votes:
            return
        
        block = Block(
            len(self.chain),
            self.pending_votes.copy(),
            self.get_latest_block().hash
        )
        block.mine_block()
        self.chain.append(block)
        self.pending_votes = []
        self.save_blockchain()  # Auto-save after mining
    
    def get_votes_for_election(self, election_id: int) -> List[Dict]:
        """Get all votes for a specific election"""
        votes = []
        for block in self.chain:
            for vote in block.votes:
                if vote["election_id"] == election_id:
                    votes.append(vote)
        return votes
    
    def get_vote_count(self, election_id: int) -> Dict[str, int]:
        """Get vote count for each option in an election"""
        votes = self.get_votes_for_election(election_id)
        vote_count = {}
        for vote in votes:
            option = vote["option"]
            vote_count[option] = vote_count.get(option, 0) + 1
        return vote_count
    
    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def save_blockchain(self):
        """Save blockchain to file"""
        try:
            os.makedirs("instance", exist_ok=True)
            with open(self.blockchain_file, 'w') as f:
                json.dump({
                    "chain": [block.to_dict() for block in self.chain],
                    "pending_votes": self.pending_votes
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving blockchain: {e}")
    
    def load_blockchain(self):
        """Load blockchain from file"""
        try:
            if os.path.exists(self.blockchain_file):
                with open(self.blockchain_file, 'r') as f:
                    data = json.load(f)
                    
                # Reconstruct blocks
                for block_data in data.get("chain", []):
                    block = Block(
                        block_data["index"],
                        block_data["votes"],
                        block_data["previous_hash"]
                    )
                    block.timestamp = block_data["timestamp"]
                    block.nonce = block_data["nonce"]
                    block.hash = block_data["hash"]
                    self.chain.append(block)
                
                self.pending_votes = data.get("pending_votes", [])
        except Exception as e:
            print(f"Error loading blockchain: {e}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert blockchain to dictionary for JSON serialization"""
        return {
            "chain": [block.to_dict() for block in self.chain],
            "pending_votes": self.pending_votes,
            "is_valid": self.is_chain_valid()
        }

# Global blockchain instance
voting_blockchain = VotingBlockchain()
