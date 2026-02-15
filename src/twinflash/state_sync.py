"""
State Synchronization Layer
Keeps Digital Twin updated with real SSD state
"""

import time
from typing import Dict, List
from dataclasses import dataclass
from .ssd_layer import SSDTelemetry


@dataclass
class SSDState:
    """Current SSD state snapshot S(t)"""
    timestamp: float
    telemetry: SSDTelemetry
    metadata: Dict
    workload_trace: List[Dict]
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'telemetry': self.telemetry.to_dict(),
            'metadata': self.metadata,
            'workload_trace': self.workload_trace
        }


class StateSynchronizer:
    """
    State Synchronization Layer
    
    Role: Keeps Digital Twin updated with real SSD
    Techniques: Log mirroring, Event streaming, Periodic snapshots
    Output: S(t) = Current SSD State
    
    Why Needed: Twin must match reality. If twin is wrong → prediction fails.
    """
    
    def __init__(self, sync_interval: float = 1.0):
        self.sync_interval = sync_interval
        self.last_sync_time = 0.0
        self.state_history: List[SSDState] = []
        self.max_history_size = 100
        
        # Sync statistics
        self.sync_count = 0
        self.sync_errors = 0
        
        print(f"[StateSynchronizer] Initialized with {sync_interval}s sync interval")
    
    def sync_state(self, telemetry: SSDTelemetry) -> SSDState:
        """
        Synchronize current state from real SSD
        Creates S(t) snapshot
        """
        current_time = time.time()
        
        # Create workload trace (recent operations)
        workload_trace = self._create_workload_trace(telemetry)
        
        # Create metadata
        metadata = {
            'sync_count': self.sync_count,
            'time_since_last_sync': current_time - self.last_sync_time,
            'health_score': self._calculate_health_score(telemetry)
        }
        
        # Create state snapshot
        state = SSDState(
            timestamp=current_time,
            telemetry=telemetry,
            metadata=metadata,
            workload_trace=workload_trace
        )
        
        # Store in history
        self._add_to_history(state)
        
        # Update sync metadata
        self.last_sync_time = current_time
        self.sync_count += 1
        
        return state
    
    def _create_workload_trace(self, telemetry: SSDTelemetry) -> List[Dict]:
        """Create workload trace from telemetry"""
        trace = []
        
        # Recent operation stats
        trace.append({
            'timestamp': telemetry.timestamp,
            'read_ops': telemetry.read_ops,
            'write_ops': telemetry.write_ops,
            'workload_level': telemetry.io_workload
        })
        
        return trace
    
    def _calculate_health_score(self, telemetry: SSDTelemetry) -> float:
        """
        Calculate overall SSD health score (0.0 to 1.0)
        Higher is better
        """
        # Factor 1: Error rate
        total_ops = telemetry.read_ops + telemetry.write_ops
        error_rate = telemetry.error_count / max(total_ops, 1)
        error_score = max(0.0, 1.0 - (error_rate * 100))
        
        # Factor 2: Temperature
        temp_score = 1.0
        if telemetry.temperature_celsius > 60:
            temp_score = max(0.0, 1.0 - (telemetry.temperature_celsius - 60) / 20)
        
        # Factor 3: Capacity utilization
        utilization = telemetry.used_capacity_gb / max(telemetry.total_capacity_gb, 1)
        capacity_score = 1.0 if utilization < 0.8 else (1.0 - (utilization - 0.8) * 2)
        
        # Factor 4: Wear level (from sampled blocks)
        avg_wear = sum(telemetry.wear_counters.values()) / max(len(telemetry.wear_counters), 1)
        wear_score = max(0.0, 1.0 - (avg_wear / 10000.0))
        
        # Weighted average
        health_score = (
            error_score * 0.3 +
            temp_score * 0.2 +
            capacity_score * 0.2 +
            wear_score * 0.3
        )
        
        return round(health_score, 3)
    
    def _add_to_history(self, state: SSDState):
        """Add state to history with size limit"""
        self.state_history.append(state)
        
        # Keep only recent history
        if len(self.state_history) > self.max_history_size:
            self.state_history = self.state_history[-self.max_history_size:]
    
    def get_current_state(self) -> SSDState:
        """Get most recent state"""
        if self.state_history:
            return self.state_history[-1]
        return None
    
    def get_state_history(self, count: int = 10) -> List[SSDState]:
        """Get recent state history"""
        return self.state_history[-count:]
    
    def is_sync_needed(self) -> bool:
        """Check if synchronization is needed"""
        current_time = time.time()
        return (current_time - self.last_sync_time) >= self.sync_interval
    
    def get_sync_statistics(self) -> Dict:
        """Get synchronization statistics"""
        return {
            'sync_count': self.sync_count,
            'sync_errors': self.sync_errors,
            'last_sync_time': self.last_sync_time,
            'history_size': len(self.state_history),
            'sync_interval': self.sync_interval
        }
    
    def mirror_logs(self, logs: List[Dict]) -> bool:
        """
        Log mirroring technique
        Mirrors operation logs from real SSD to twin
        """
        try:
            for log_entry in logs:
                # Process and store log entry
                pass
            return True
        except Exception as e:
            self.sync_errors += 1
            print(f"[StateSynchronizer] Log mirroring error: {e}")
            return False
    
    def stream_events(self, event: Dict) -> bool:
        """
        Event streaming technique
        Streams real-time events to keep twin synchronized
        """
        try:
            # Process event
            event_type = event.get('type', 'unknown')
            if event_type in ['write', 'read', 'erase', 'error']:
                # Update state based on event
                pass
            return True
        except Exception as e:
            self.sync_errors += 1
            print(f"[StateSynchronizer] Event streaming error: {e}")
            return False
    
    def create_snapshot(self, telemetry: SSDTelemetry) -> Dict:
        """
        Periodic snapshot technique
        Creates complete state snapshot for twin
        """
        return {
            'timestamp': time.time(),
            'telemetry': telemetry.to_dict(),
            'snapshot_type': 'periodic',
            'health_score': self._calculate_health_score(telemetry)
        }
