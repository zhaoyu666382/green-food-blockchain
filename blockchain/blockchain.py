import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid


class Block:
    """A minimal block implementation (teaching/demo use)."""

    def __init__(
        self,
        index: int,
        timestamp: str,
        data: Dict[str, Any],
        previous_hash: str,
        nonce: int = 0,
        block_hash: Optional[str] = None,
    ):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = block_hash or self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps(
            {
                "index": self.index,
                "timestamp": self.timestamp,
                "data": self.data,
                "previous_hash": self.previous_hash,
                "nonce": self.nonce,
            },
            sort_keys=True,
            ensure_ascii=False,
        )
        return hashlib.sha256(block_string.encode("utf-8")).hexdigest()

    def mine(self, difficulty: int) -> None:
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Block":
        return Block(
            index=int(d["index"]),
            timestamp=d["timestamp"],
            data=d["data"],
            previous_hash=d["previous_hash"],
            nonce=int(d.get("nonce", 0)),
            block_hash=d.get("hash"),
        )


class Blockchain:
    """A lightweight blockchain with PoW and JSON persistence hooks."""

    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Dict[str, Any]] = []
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        genesis_block = Block(
            index=0,
            timestamp=datetime.utcnow().isoformat(),
            data={"message": "Genesis Block - Green Food Platform"},
            previous_hash="0",
        )
        genesis_block.mine(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, tx: Dict[str, Any]) -> str:
        tx_id = str(uuid.uuid4())
        self.pending_transactions.append({"tx_id": tx_id, "payload": tx, "created_at": datetime.utcnow().isoformat()})
        return tx_id

    def mine_pending_transactions(self, miner_address: str = "system") -> Dict[str, Any]:
        if not self.pending_transactions:
            raise ValueError("No pending transactions")

        block_data = {
            "transactions": self.pending_transactions,
            "miner": miner_address,
        }
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.utcnow().isoformat(),
            data=block_data,
            previous_hash=self.get_latest_block().hash,
        )
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block.to_dict()

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != prev.hash:
                return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "difficulty": self.difficulty,
            "chain": [b.to_dict() for b in self.chain],
            "pending_transactions": self.pending_transactions,
        }

    def load_from_dict(self, d: Dict[str, Any]) -> None:
        self.difficulty = int(d.get("difficulty", self.difficulty))
        self.chain = [Block.from_dict(x) for x in d.get("chain", [])] or []
        if not self.chain:
            self.create_genesis_block()
        self.pending_transactions = d.get("pending_transactions", [])
