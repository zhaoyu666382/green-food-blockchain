import json
from pathlib import Path
from typing import Any, Dict, Optional

from blockchain.blockchain import Blockchain

DEFAULT_CHAIN_PATH = Path("./data/blockchain_chain.json")


class BlockchainService:
    """A lightweight local-ledger service for demo & teaching purposes.

    - Persists chain to a JSON file
    - Provides 'anchor' hash for trace events/batches
    """

    def __init__(self, chain_path: Path = DEFAULT_CHAIN_PATH, difficulty: int = 2):
        self.chain_path = chain_path
        self.chain_path.parent.mkdir(parents=True, exist_ok=True)
        self.bc = Blockchain(difficulty=difficulty)
        self._load_if_exists()

    def _load_if_exists(self) -> None:
        if not self.chain_path.exists():
            self._save()
            return
        try:
            data = json.loads(self.chain_path.read_text(encoding="utf-8"))
            self.bc.load_from_dict(data)
        except Exception:
            # If file corrupted, keep fresh chain but do not crash app
            self._save()

    def _save(self) -> None:
        self.chain_path.write_text(json.dumps(self.bc.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    def anchor(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Append one trace transaction and mine a block immediately (simple demo mode)."""
        tx_id = self.bc.add_transaction(payload)
        block = self.bc.mine_pending_transactions(miner_address="system")
        self._save()
        return {"tx_id": tx_id, "block_hash": block["hash"], "block_index": block["index"], "timestamp": block["timestamp"]}

    def verify_chain(self) -> bool:
        return self.bc.is_chain_valid()
