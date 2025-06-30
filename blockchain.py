import hashlib
import json
import os
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any

# Zona horaria de Perú (UTC-5)
PERU_TZ = timezone(timedelta(hours=-5))

class Block:
    """Bloque individual en la cadena de bloques"""
    
    def __init__(self, index: int, votes: List[Dict], previous_hash: str):
        self.index = index
        self.timestamp = datetime.now(PERU_TZ).isoformat()
        self.votes = votes  # List of anonymous votes
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calcula hash del bloque"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "votes": self.votes,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 4):
        """Mina el bloque hasta que cumpla con la dificultad"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el bloque a un diccionario para serialización JSON"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "votes": self.votes,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }

class VotingBlockchain:
    """Implementación de la cadena de bloques para el sistema de votación"""
    
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
        now_peru = datetime.now(PERU_TZ)
        vote = {
            "election_id": election_id,
            "option": option,
            "timestamp": now_peru.isoformat(),
            "vote_id": hashlib.sha256(f"{election_id}{option}{now_peru}".encode()).hexdigest()[:16]
        }
        self.pending_votes.append(vote)
    
    def mine_pending_votes(self):
        """Mina todos los votos pendientes en un nuevo bloque"""
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
        """Obtiene todos los votos para una elección específica"""
        votes = []
        for block in self.chain:
            for vote in block.votes:
                if vote["election_id"] == election_id:
                    votes.append(vote)
        return votes
    
    def get_vote_count(self, election_id: int) -> Dict[str, int]:
        """Obtiene el conteo de votos para una elección específica"""
        votes = self.get_votes_for_election(election_id)
        vote_count = {}
        for vote in votes:
            option = vote["option"]
            vote_count[option] = vote_count.get(option, 0) + 1
        return vote_count
    
    def is_chain_valid(self) -> bool:
        """Valida la cadena de bloques"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def save_blockchain(self):
        """Guarda la cadena de bloques en un archivo"""
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
        """Carga la cadena de bloques desde un archivo"""
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
    
    def remove_votes_for_election(self, election_id: int):
        """Elimina todos los votos para una elección específica de la blockchain"""
        # Filtrar votos pendientes
        self.pending_votes = [vote for vote in self.pending_votes if vote["election_id"] != election_id]
        
        # Crear nueva cadena sin los votos de la elección eliminada
        new_chain = []
        
        for block in self.chain:
            if block.index == 0:  # Genesis block
                new_chain.append(block)
                continue
            
            # Filtrar votos del bloque
            filtered_votes = [vote for vote in block.votes if vote["election_id"] != election_id]
            
            # Solo agregar bloques que tengan votos después del filtrado
            if filtered_votes:
                new_block = Block(
                    len(new_chain),
                    filtered_votes,
                    new_chain[-1].hash if new_chain else "0"
                )
                new_block.mine_block()
                new_chain.append(new_block)
        
        self.chain = new_chain
        self.save_blockchain()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la cadena de bloques a un diccionario para serialización JSON"""
        return {
            "chain": [block.to_dict() for block in self.chain],
            "pending_votes": self.pending_votes,
            "is_valid": self.is_chain_valid()
        }

# Instancia global de la cadena de bloques
voting_blockchain = VotingBlockchain()
