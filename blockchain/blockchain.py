import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any

class Block:
    """区块类"""
    
    def __init__(self, index: int, timestamp: str, data: Dict[Any, Any], 
                 previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """计算区块哈希值"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int):
        """工作量证明挖矿"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"✅ 区块已挖出: {self.hash}")
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }

class Blockchain:
    """区块链类"""
    
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Dict] = []
        self.mining_reward = 10
        
        # 创建创世区块
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """创建创世区块"""
        genesis_block = Block(
            index=0,
            timestamp=datetime.now().isoformat(),
            data={"message": "创世区块 - 绿色食品交易平台"},
            previous_hash="0"
        )
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        print("🎉 创世区块已创建")
    
    def get_latest_block(self) -> Block:
        """获取最新区块"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Dict):
        """添加交易到待处理列表"""
        # 验证交易
        if not transaction.get("from") or not transaction.get("to"):
            raise ValueError("交易必须包含发送方和接收方")
        
        self.pending_transactions.append(transaction)
        print(f"📝 交易已添加到待处理列表")
    
    def mine_pending_transactions(self, miner_address: str):
        """挖矿处理待处理的交易"""
        if not self.pending_transactions:
            print("⚠️  没有待处理的交易")
            return
        
        # 创建新区块
        block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            data={"transactions": self.pending_transactions},
            previous_hash=self.get_latest_block().hash
        )
        
        # 挖矿
        block.mine_block(self.difficulty)
        
        # 添加到链
        self.chain.append(block)
        print(f"✅ 区块 #{block.index} 已添加到链上")
        
        # 清空待处理交易，添加挖矿奖励交易
        self.pending_transactions = [{
            "from": "system",
            "to": miner_address,
            "amount": self.mining_reward,
            "type": "mining_reward"
        }]
    
    def add_trace_event(self, event_data: Dict):
        """添加溯源事件"""
        block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            data=event_data,
            previous_hash=self.get_latest_block().hash
        )
        
        block.mine_block(self.difficulty)
        self.chain.append(block)
        
        print(f"🔗 溯源事件已上链: {event_data.get('event_type')}")
        return block.hash
    
    def is_chain_valid(self) -> bool:
        """验证区块链完整性"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # 验证当前区块哈希
            if current_block.hash != current_block.calculate_hash():
                print(f"❌ 区块 #{i} 哈希值无效")
                return False
            
            # 验证链接
            if current_block.previous_hash != previous_block.hash:
                print(f"❌ 区块 #{i} 与前一区块链接断裂")
                return False
        
        print("✅ 区块链验证通过")
        return True
    
    def get_balance(self, address: str) -> float:
        """获取地址余额"""
        balance = 0
        
        for block in self.chain:
            if "transactions" in block.data:
                for tx in block.data["transactions"]:
                    if tx.get("from") == address:
                        balance -= tx.get("amount", 0)
                    if tx.get("to") == address:
                        balance += tx.get("amount", 0)
        
        return balance
    
    def get_trace_history(self, batch_number: str) -> List[Dict]:
        """获取批次溯源历史"""
        trace_history = []
        
        for block in self.chain:
            if block.data.get("batch_number") == batch_number:
                trace_history.append(block.to_dict())
        
        return trace_history
    
    def to_dict(self) -> List[Dict]:
        """转换整个链为字典列表"""
        return [block.to_dict() for block in self.chain]
    
    def print_chain(self):
        """打印区块链"""
        print("\n" + "="*50)
        print("🔗 区块链信息")
        print("="*50)
        for block in self.chain:
            print(f"\n区块 #{block.index}")
            print(f"时间戳: {block.timestamp}")
            print(f"前一区块哈希: {block.previous_hash}")
            print(f"当前区块哈希: {block.hash}")
            print(f"Nonce: {block.nonce}")
            print(f"数据: {json.dumps(block.data, ensure_ascii=False, indent=2)}")
        print("="*50 + "\n")

# 测试代码
if __name__ == "__main__":
    # 创建区块链
    bc = Blockchain(difficulty=2)
    
    # 添加溯源事件
    bc.add_trace_event({
        "batch_number": "BATCH-2025-001",
        "event_type": "种植",
        "product_name": "有机白菜",
        "location": "江西省南昌市东华理工大学农场",
        "operator": "张三",
        "description": "开始种植有机白菜"
    })
    
    bc.add_trace_event({
        "batch_number": "BATCH-2025-001",
        "event_type": "采摘",
        "product_name": "有机白菜",
        "location": "江西省南昌市东华理工大学农场",
        "operator": "李四",
        "description": "完成采摘，准备包装"
    })
    
    # 打印区块链
    bc.print_chain()
    
    # 验证区块链
    bc.is_chain_valid()
    
    # 获取溯源历史
    history = bc.get_trace_history("BATCH-2025-001")
    print(f"\n📦 批次 BATCH-2025-001 溯源记录: {len(history)} 条")
