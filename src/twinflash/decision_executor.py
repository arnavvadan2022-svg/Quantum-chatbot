"""
Decision & Execution Layer
Applies AI decision to real SSD with safety mechanisms
"""

import time
from typing import Dict, Optional
from .rl_engine import Action
from .ssd_layer import RealSSDLayer


class DecisionExecutor:
    """
    Decision & Execution Layer
    
    Role: Applies AI decision to real SSD
    Actions: Sends firmware command, Triggers compression, Adjusts GC, Updates mapping
    Safety Mechanism: If confidence < threshold → fallback rules
    
    Prevents risky actions
    """
    
    def __init__(self, ssd_layer: RealSSDLayer, safety_threshold: float = 0.7):
        self.ssd = ssd_layer
        self.safety_threshold = safety_threshold
        
        # Execution statistics
        self.executed_actions = 0
        self.blocked_actions = 0
        self.fallback_actions = 0
        
        # Execution history
        self.execution_history = []
        self.max_history = 100
        
        print(f"[DecisionExecutor] Initialized with safety threshold {safety_threshold}")
    
    def execute(self, action: Action, confidence: float, predicted_metrics: Dict) -> Dict:
        """
        Execute action on real SSD with safety checks
        
        Returns: execution_result dict with status and metrics
        """
        print(f"\n[DecisionExecutor] Executing: {action.name} (confidence={confidence:.2f})")
        
        # Safety check
        if not self._is_safe_to_execute(action, confidence, predicted_metrics):
            print(f"  ⚠️  Action blocked by safety mechanism")
            return self._execute_fallback(action)
        
        # Execute the action
        result = self._execute_action(action)
        
        # Record execution
        execution_record = {
            'timestamp': time.time(),
            'action': action.name,
            'parameters': action.parameters,
            'confidence': confidence,
            'result': result,
            'status': result['status']
        }
        self._add_to_history(execution_record)
        
        if result['status'] == 'success':
            self.executed_actions += 1
            print(f"  ✓ Action executed successfully")
        else:
            print(f"  ✗ Action execution failed: {result.get('error', 'Unknown error')}")
        
        return result
    
    def _is_safe_to_execute(self, action: Action, confidence: float, metrics: Dict) -> bool:
        """
        Safety mechanism: Check if action is safe to execute
        
        Returns False if:
        - Confidence too low
        - Predicted metrics indicate high risk
        - Action would cause critical damage
        """
        # Check 1: Confidence threshold
        if confidence < self.safety_threshold:
            print(f"    Safety: Confidence too low ({confidence:.2f} < {self.safety_threshold})")
            return False
        
        # Check 2: Wear level safety
        if 'wear' in metrics and metrics['wear'] < 0.3:  # Very high wear
            print(f"    Safety: Wear level too high ({metrics['wear']:.2f})")
            return False
        
        # Check 3: Error rate safety
        if 'error' in metrics and metrics['error'] < 0.5:  # High error rate
            print(f"    Safety: Error rate too high ({metrics['error']:.2f})")
            return False
        
        # Check 4: Latency impact
        if 'latency' in metrics and metrics['latency'] < 0.3:  # Very slow
            print(f"    Safety: Latency impact too high ({metrics['latency']:.2f})")
            # This is a warning, not a blocker
            pass
        
        return True
    
    def _execute_action(self, action: Action) -> Dict:
        """Execute specific action on real SSD"""
        try:
            if action.name == 'compress_now':
                return self._execute_compression(action.parameters)
            
            elif action.name == 'delay_compress':
                return self._execute_delay_compression(action.parameters)
            
            elif action.name == 'migrate_block':
                return self._execute_block_migration(action.parameters)
            
            elif action.name == 'reallocate':
                return self._execute_reallocation(action.parameters)
            
            elif action.name == 'gc_trigger':
                return self._execute_garbage_collection(action.parameters)
            
            else:
                return {
                    'status': 'error',
                    'error': f'Unknown action: {action.name}'
                }
        
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _execute_compression(self, parameters: Dict) -> Dict:
        """Execute data compression on SSD"""
        # Simulate compression by reducing write operations
        compression_level = parameters.get('compression_level', 6)
        
        # In real system, would send firmware command
        # For simulation, we just record the action
        
        return {
            'status': 'success',
            'action': 'compression',
            'compression_level': compression_level,
            'estimated_space_saved': '20-30%',
            'overhead_ms': 5.0
        }
    
    def _execute_delay_compression(self, parameters: Dict) -> Dict:
        """Delay compression execution"""
        delay_hours = parameters.get('delay_hours', 4)
        
        return {
            'status': 'success',
            'action': 'delay_compression',
            'delay_hours': delay_hours,
            'scheduled_time': time.time() + (delay_hours * 3600)
        }
    
    def _execute_block_migration(self, parameters: Dict) -> Dict:
        """Execute block migration to healthier blocks"""
        target_blocks = parameters.get('target_blocks', 'low_wear')
        
        # Simulate migration by moving data between blocks
        # In real system, would update flash translation layer (FTL)
        
        migrated_blocks = 0
        for block_id in range(10):  # Migrate 10 blocks as example
            if self.ssd.blocks[block_id]['status'] == 'used':
                # Find target block with low wear
                target_id = self._find_low_wear_block()
                if target_id is not None:
                    # Simulate migration
                    self.ssd.read_block(block_id)
                    self.ssd.write_block(target_id)
                    self.ssd.erase_block(block_id)
                    migrated_blocks += 1
        
        return {
            'status': 'success',
            'action': 'block_migration',
            'migrated_blocks': migrated_blocks,
            'target_strategy': target_blocks
        }
    
    def _execute_reallocation(self, parameters: Dict) -> Dict:
        """Execute block reallocation for wear leveling"""
        strategy = parameters.get('strategy', 'wear_leveling')
        
        # Simulate wear leveling by redistributing data
        reallocated_blocks = 5  # Example
        
        return {
            'status': 'success',
            'action': 'reallocation',
            'strategy': strategy,
            'reallocated_blocks': reallocated_blocks
        }
    
    def _execute_garbage_collection(self, parameters: Dict) -> Dict:
        """Execute garbage collection"""
        aggressive = parameters.get('aggressive', False)
        
        # Simulate GC by reclaiming free blocks
        reclaimed_blocks = 0
        for block_id in range(20):  # Check 20 blocks
            if self.ssd.blocks[block_id]['status'] == 'used':
                # In real system, check if block can be reclaimed
                if aggressive or block_id % 2 == 0:  # Aggressive GC reclaims more
                    self.ssd.erase_block(block_id)
                    reclaimed_blocks += 1
        
        return {
            'status': 'success',
            'action': 'garbage_collection',
            'aggressive': aggressive,
            'reclaimed_blocks': reclaimed_blocks,
            'gc_overhead_ms': 50.0 if aggressive else 25.0
        }
    
    def _execute_fallback(self, action: Action) -> Dict:
        """Execute safe fallback action when primary action blocked"""
        self.fallback_actions += 1
        self.blocked_actions += 1
        
        # Fallback: Always choose the safest option (delay)
        print("  → Executing fallback: delay_compress")
        
        fallback_action = Action(
            name='delay_compress',
            parameters={'delay_hours': 2},
            description='Safe fallback action'
        )
        
        result = self._execute_action(fallback_action)
        result['fallback'] = True
        result['original_action'] = action.name
        
        return result
    
    def _find_low_wear_block(self) -> Optional[int]:
        """Find a block with low wear count"""
        min_wear = float('inf')
        best_block = None
        
        for block_id, block_info in self.ssd.blocks.items():
            if block_info['status'] == 'free' and block_info['wear_count'] < min_wear:
                min_wear = block_info['wear_count']
                best_block = block_id
        
        return best_block
    
    def _add_to_history(self, record: Dict):
        """Add execution record to history"""
        self.execution_history.append(record)
        
        if len(self.execution_history) > self.max_history:
            self.execution_history = self.execution_history[-self.max_history:]
    
    def get_statistics(self) -> Dict:
        """Get execution statistics"""
        success_rate = 0.0
        if self.executed_actions + self.blocked_actions > 0:
            success_rate = self.executed_actions / (self.executed_actions + self.blocked_actions)
        
        return {
            'total_executed': self.executed_actions,
            'total_blocked': self.blocked_actions,
            'fallback_count': self.fallback_actions,
            'success_rate': round(success_rate, 3),
            'history_size': len(self.execution_history)
        }
    
    def get_execution_history(self, count: int = 10) -> list:
        """Get recent execution history"""
        return self.execution_history[-count:]
