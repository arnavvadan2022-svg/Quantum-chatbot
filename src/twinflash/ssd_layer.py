"""
Real SSD Layer (Physical Layer)
Provides live storage telemetry from actual SSD devices
"""

import time
import random
from typing import Dict, List
from dataclasses import dataclass, asdict


@dataclass
class SSDTelemetry:
    """Live storage telemetry data"""
    timestamp: float
    read_ops: int
    write_ops: int
    block_status: Dict[int, str]  # block_id -> status (free, used, bad)
    wear_counters: Dict[int, int]  # block_id -> erase_count
    error_count: int
    temperature_celsius: float
    io_workload: float  # 0.0 to 1.0
    total_capacity_gb: int
    used_capacity_gb: int
    
    def to_dict(self):
        return asdict(self)


class RealSSDLayer:
    """
    Real SSD Layer - Physical Layer
    
    Role: Interface with actual storage device
    Provides: Read/write ops, block status, wear counters, error logs, 
              temperature data, I/O workload
    Output: Live Storage Telemetry
    """
    
    def __init__(self, capacity_gb: int = 256, num_blocks: int = 1000):
        self.capacity_gb = capacity_gb
        self.num_blocks = num_blocks
        self.blocks = {i: {'status': 'free', 'wear_count': 0} for i in range(num_blocks)}
        
        # Operational metrics
        self.read_ops = 0
        self.write_ops = 0
        self.error_count = 0
        self.temperature = 45.0  # Celsius
        self.used_blocks = 0
        
        print(f"[RealSSDLayer] Initialized {capacity_gb}GB SSD with {num_blocks} blocks")
    
    def read_block(self, block_id: int) -> bool:
        """Simulate block read operation"""
        if 0 <= block_id < self.num_blocks:
            self.read_ops += 1
            # Simulate potential read error
            if random.random() < 0.001:  # 0.1% error rate
                self.error_count += 1
                return False
            return True
        return False
    
    def write_block(self, block_id: int) -> bool:
        """Simulate block write operation"""
        if 0 <= block_id < self.num_blocks:
            self.write_ops += 1
            self.blocks[block_id]['wear_count'] += 1
            
            if self.blocks[block_id]['status'] == 'free':
                self.blocks[block_id]['status'] = 'used'
                self.used_blocks += 1
            
            # Simulate potential write error
            if random.random() < 0.002:  # 0.2% error rate
                self.error_count += 1
                return False
            
            # Simulate block degradation
            if self.blocks[block_id]['wear_count'] > 10000:
                self.blocks[block_id]['status'] = 'bad'
            
            return True
        return False
    
    def erase_block(self, block_id: int) -> bool:
        """Simulate block erase operation (wear inducing)"""
        if 0 <= block_id < self.num_blocks:
            self.blocks[block_id]['wear_count'] += 1
            self.blocks[block_id]['status'] = 'free'
            if self.used_blocks > 0:
                self.used_blocks -= 1
            return True
        return False
    
    def get_telemetry(self) -> SSDTelemetry:
        """
        Collect current SSD telemetry
        This is what the AI needs to make decisions
        """
        # Update temperature based on workload
        workload = self.calculate_workload()
        self.temperature = 45.0 + (workload * 20.0)  # 45-65°C range
        
        # Collect block status
        block_status = {
            block_id: self.blocks[block_id]['status'] 
            for block_id in range(min(100, self.num_blocks))  # Sample first 100
        }
        
        # Collect wear counters
        wear_counters = {
            block_id: self.blocks[block_id]['wear_count']
            for block_id in range(min(100, self.num_blocks))  # Sample first 100
        }
        
        used_capacity = int((self.used_blocks / self.num_blocks) * self.capacity_gb)
        
        return SSDTelemetry(
            timestamp=time.time(),
            read_ops=self.read_ops,
            write_ops=self.write_ops,
            block_status=block_status,
            wear_counters=wear_counters,
            error_count=self.error_count,
            temperature_celsius=round(self.temperature, 2),
            io_workload=round(workload, 3),
            total_capacity_gb=self.capacity_gb,
            used_capacity_gb=used_capacity
        )
    
    def calculate_workload(self) -> float:
        """Calculate current I/O workload (0.0 to 1.0)"""
        total_ops = self.read_ops + self.write_ops
        # Normalize to 0-1 range (assuming max 10000 ops per interval)
        workload = min(1.0, (total_ops % 10000) / 10000.0)
        return workload
    
    def get_block_info(self, block_id: int) -> Dict:
        """Get detailed information about a specific block"""
        if 0 <= block_id < self.num_blocks:
            return {
                'block_id': block_id,
                'status': self.blocks[block_id]['status'],
                'wear_count': self.blocks[block_id]['wear_count'],
                'degradation_level': min(1.0, self.blocks[block_id]['wear_count'] / 10000.0)
            }
        return {}
    
    def simulate_workload(self, num_operations: int = 100):
        """Simulate random SSD workload for testing"""
        for _ in range(num_operations):
            op_type = random.choice(['read', 'write', 'erase'])
            block_id = random.randint(0, self.num_blocks - 1)
            
            if op_type == 'read':
                self.read_block(block_id)
            elif op_type == 'write':
                self.write_block(block_id)
            else:
                self.erase_block(block_id)
        
        print(f"[RealSSDLayer] Simulated {num_operations} operations")
    
    def get_statistics(self) -> Dict:
        """Get overall SSD statistics"""
        total_wear = sum(block['wear_count'] for block in self.blocks.values())
        avg_wear = total_wear / self.num_blocks
        
        bad_blocks = sum(1 for block in self.blocks.values() if block['status'] == 'bad')
        used_blocks = sum(1 for block in self.blocks.values() if block['status'] == 'used')
        free_blocks = sum(1 for block in self.blocks.values() if block['status'] == 'free')
        
        return {
            'total_operations': self.read_ops + self.write_ops,
            'read_ops': self.read_ops,
            'write_ops': self.write_ops,
            'error_count': self.error_count,
            'temperature_celsius': round(self.temperature, 2),
            'average_wear': round(avg_wear, 2),
            'blocks': {
                'total': self.num_blocks,
                'free': free_blocks,
                'used': used_blocks,
                'bad': bad_blocks
            },
            'capacity': {
                'total_gb': self.capacity_gb,
                'used_gb': int((used_blocks / self.num_blocks) * self.capacity_gb),
                'free_gb': int((free_blocks / self.num_blocks) * self.capacity_gb)
            }
        }
