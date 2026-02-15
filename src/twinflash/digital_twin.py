"""
Digital Twin Layer (Simulation Engine)
Creates a virtual SSD in software to predict future states
"""

import time
import random
from typing import Dict, List, Tuple
from dataclasses import dataclass
from .state_sync import SSDState


@dataclass
class PredictedState:
    """Predicted future state S(t+1)"""
    timestamp: float
    predicted_wear: Dict[int, float]
    predicted_latency: float
    predicted_errors: int
    predicted_lifetime_hours: float
    confidence: float
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'predicted_wear': self.predicted_wear,
            'predicted_latency': self.predicted_latency,
            'predicted_errors': self.predicted_errors,
            'predicted_lifetime_hours': self.predicted_lifetime_hours,
            'confidence': self.confidence
        }


class WearModel:
    """
    Wear Model - Predicts block degradation
    """
    
    def __init__(self):
        self.max_erase_cycles = 10000  # Typical SSD limit
    
    def predict_wear_impact(self, current_wear: int, operations: int) -> float:
        """Predict wear impact from operations"""
        # Each write/erase increments wear counter
        predicted_wear = current_wear + (operations * 0.1)  # 10% of ops cause wear
        
        # Calculate degradation level
        degradation = min(1.0, predicted_wear / self.max_erase_cycles)
        
        return degradation
    
    def predict_block_lifetime(self, current_wear: int, avg_ops_per_hour: int) -> float:
        """Predict remaining lifetime of block in hours"""
        remaining_cycles = max(0, self.max_erase_cycles - current_wear)
        
        if avg_ops_per_hour == 0:
            return float('inf')
        
        # Estimate hours until failure
        hours_remaining = remaining_cycles / (avg_ops_per_hour * 0.1)
        return hours_remaining


class LatencyModel:
    """
    Latency Model - Predicts read/write delays
    """
    
    def __init__(self):
        self.base_read_latency = 0.1  # ms
        self.base_write_latency = 0.5  # ms
    
    def predict_read_latency(self, workload: float, queue_depth: int) -> float:
        """Predict read latency based on workload and queue depth"""
        # Latency increases with workload and queue congestion
        latency = self.base_read_latency * (1 + workload) * (1 + queue_depth * 0.1)
        return round(latency, 3)
    
    def predict_write_latency(self, workload: float, queue_depth: int, wear_level: float) -> float:
        """Predict write latency considering wear level"""
        # Write latency affected by wear (degraded blocks slower)
        latency = self.base_write_latency * (1 + workload) * (1 + queue_depth * 0.1) * (1 + wear_level * 0.5)
        return round(latency, 3)
    
    def predict_queue_congestion(self, current_ops: int, capacity: int) -> int:
        """Predict queue depth based on operation load"""
        queue_depth = int((current_ops / max(capacity, 1)) * 10)
        return min(queue_depth, 100)  # Max queue of 100


class ErrorModel:
    """
    Error Model - Predicts bit errors and failures
    """
    
    def __init__(self):
        self.base_error_rate = 0.001  # 0.1%
    
    def predict_bit_error_rate(self, wear_level: float, temperature: float) -> float:
        """Predict bit error rate based on wear and temperature"""
        # Error rate increases with wear and high temperature
        temp_factor = 1.0 + max(0, (temperature - 60) / 20.0)  # Increase above 60°C
        wear_factor = 1.0 + (wear_level * 2.0)  # Double at max wear
        
        error_rate = self.base_error_rate * temp_factor * wear_factor
        return min(error_rate, 0.1)  # Cap at 10%
    
    def predict_retention_loss(self, age_hours: float, temperature: float) -> float:
        """Predict data retention loss"""
        # Data retention degrades over time, especially at high temp
        retention_factor = 1.0 - (age_hours / (10 * 365 * 24))  # 10 year lifetime
        temp_impact = max(0, (temperature - 70) / 30.0)  # Significant above 70°C
        
        retention = retention_factor * (1.0 - temp_impact * 0.2)
        return max(0.0, retention)
    
    def predict_ecc_failure(self, error_rate: float) -> bool:
        """Predict if ECC will fail to correct errors"""
        # ECC typically handles up to 1% error rate
        return error_rate > 0.01


class DigitalTwin:
    """
    Digital Twin Layer - Simulation Engine
    
    Role: Creates a virtual SSD in software
    Internal Modules: Wear Model, Latency Model, Error Model
    Input: Current State S(t)
    Output: Predicted State S(t+1)
    
    Why Needed: This is the "future generator"
    """
    
    def __init__(self):
        self.wear_model = WearModel()
        self.latency_model = LatencyModel()
        self.error_model = ErrorModel()
        
        # Twin state
        self.virtual_state = None
        self.prediction_history = []
        
        print("[DigitalTwin] Simulation engine initialized")
    
    def sync_from_real(self, current_state: SSDState):
        """Synchronize twin with real SSD state"""
        self.virtual_state = current_state
        print(f"[DigitalTwin] Synced with real SSD at t={current_state.timestamp}")
    
    def simulate_action(self, action: str, parameters: Dict) -> PredictedState:
        """
        Simulate an action and predict future state
        This is the core "what-if" simulation
        """
        if not self.virtual_state:
            raise ValueError("Twin not synchronized with real SSD")
        
        telemetry = self.virtual_state.telemetry
        
        # Simulate different actions
        if action == 'compress_now':
            return self._simulate_compression(telemetry, parameters)
        elif action == 'delay_compress':
            return self._simulate_delayed_compression(telemetry, parameters)
        elif action == 'migrate_block':
            return self._simulate_block_migration(telemetry, parameters)
        elif action == 'reallocate':
            return self._simulate_reallocation(telemetry, parameters)
        elif action == 'gc_trigger':
            return self._simulate_garbage_collection(telemetry, parameters)
        else:
            return self._simulate_no_action(telemetry)
    
    def _simulate_compression(self, telemetry, parameters) -> PredictedState:
        """Simulate immediate compression action"""
        # Compression reduces writes but adds CPU load
        
        # Calculate wear impact (fewer writes = less wear)
        avg_wear = sum(telemetry.wear_counters.values()) / max(len(telemetry.wear_counters), 1)
        compression_benefit = 0.3  # 30% reduction in writes
        predicted_wear = {
            block_id: wear * (1 - compression_benefit)
            for block_id, wear in list(telemetry.wear_counters.items())[:10]
        }
        
        # Latency increases slightly due to compression overhead
        queue_depth = self.latency_model.predict_queue_congestion(
            telemetry.read_ops + telemetry.write_ops, 1000
        )
        predicted_latency = self.latency_model.predict_write_latency(
            telemetry.io_workload, queue_depth, avg_wear / 10000
        ) * 1.2  # 20% overhead
        
        # Estimate lifetime improvement
        ops_per_hour = (telemetry.read_ops + telemetry.write_ops) / 24  # Rough estimate
        predicted_lifetime = self.wear_model.predict_block_lifetime(
            int(avg_wear * (1 - compression_benefit)), int(ops_per_hour)
        )
        
        return PredictedState(
            timestamp=time.time(),
            predicted_wear=predicted_wear,
            predicted_latency=predicted_latency,
            predicted_errors=telemetry.error_count,
            predicted_lifetime_hours=predicted_lifetime,
            confidence=0.85
        )
    
    def _simulate_delayed_compression(self, telemetry, parameters) -> PredictedState:
        """Simulate delayed compression action"""
        # No immediate overhead, but wear continues
        
        avg_wear = sum(telemetry.wear_counters.values()) / max(len(telemetry.wear_counters), 1)
        predicted_wear = {
            block_id: wear * 1.1  # Wear continues
            for block_id, wear in list(telemetry.wear_counters.items())[:10]
        }
        
        queue_depth = self.latency_model.predict_queue_congestion(
            telemetry.read_ops + telemetry.write_ops, 1000
        )
        predicted_latency = self.latency_model.predict_write_latency(
            telemetry.io_workload, queue_depth, avg_wear / 10000
        )
        
        ops_per_hour = (telemetry.read_ops + telemetry.write_ops) / 24
        predicted_lifetime = self.wear_model.predict_block_lifetime(
            int(avg_wear * 1.1), int(ops_per_hour)
        )
        
        return PredictedState(
            timestamp=time.time(),
            predicted_wear=predicted_wear,
            predicted_latency=predicted_latency,
            predicted_errors=telemetry.error_count,
            predicted_lifetime_hours=predicted_lifetime,
            confidence=0.90
        )
    
    def _simulate_block_migration(self, telemetry, parameters) -> PredictedState:
        """Simulate block migration to healthier blocks"""
        # Migration reduces wear on heavily used blocks
        
        avg_wear = sum(telemetry.wear_counters.values()) / max(len(telemetry.wear_counters), 1)
        migration_benefit = 0.2
        predicted_wear = {
            block_id: wear * (1 - migration_benefit) if wear > avg_wear else wear
            for block_id, wear in list(telemetry.wear_counters.items())[:10]
        }
        
        # Migration has overhead
        queue_depth = self.latency_model.predict_queue_congestion(
            telemetry.read_ops + telemetry.write_ops, 1000
        )
        predicted_latency = self.latency_model.predict_write_latency(
            telemetry.io_workload, queue_depth + 5, avg_wear / 10000
        )
        
        ops_per_hour = (telemetry.read_ops + telemetry.write_ops) / 24
        predicted_lifetime = self.wear_model.predict_block_lifetime(
            int(avg_wear * (1 - migration_benefit)), int(ops_per_hour)
        )
        
        return PredictedState(
            timestamp=time.time(),
            predicted_wear=predicted_wear,
            predicted_latency=predicted_latency,
            predicted_errors=telemetry.error_count,
            predicted_lifetime_hours=predicted_lifetime,
            confidence=0.80
        )
    
    def _simulate_reallocation(self, telemetry, parameters) -> PredictedState:
        """Simulate block reallocation"""
        avg_wear = sum(telemetry.wear_counters.values()) / max(len(telemetry.wear_counters), 1)
        predicted_wear = {
            block_id: wear * 0.95  # Slight improvement
            for block_id, wear in list(telemetry.wear_counters.items())[:10]
        }
        
        queue_depth = self.latency_model.predict_queue_congestion(
            telemetry.read_ops + telemetry.write_ops, 1000
        )
        predicted_latency = self.latency_model.predict_write_latency(
            telemetry.io_workload, queue_depth, avg_wear / 10000
        )
        
        ops_per_hour = (telemetry.read_ops + telemetry.write_ops) / 24
        predicted_lifetime = self.wear_model.predict_block_lifetime(
            int(avg_wear * 0.95), int(ops_per_hour)
        )
        
        return PredictedState(
            timestamp=time.time(),
            predicted_wear=predicted_wear,
            predicted_latency=predicted_latency,
            predicted_errors=telemetry.error_count,
            predicted_lifetime_hours=predicted_lifetime,
            confidence=0.82
        )
    
    def _simulate_garbage_collection(self, telemetry, parameters) -> PredictedState:
        """Simulate garbage collection trigger"""
        # GC has high overhead but improves long-term performance
        
        avg_wear = sum(telemetry.wear_counters.values()) / max(len(telemetry.wear_counters), 1)
        predicted_wear = {
            block_id: wear * 1.05  # GC causes some wear
            for block_id, wear in list(telemetry.wear_counters.items())[:10]
        }
        
        queue_depth = self.latency_model.predict_queue_congestion(
            telemetry.read_ops + telemetry.write_ops, 1000
        )
        predicted_latency = self.latency_model.predict_write_latency(
            telemetry.io_workload, queue_depth + 10, avg_wear / 10000
        ) * 1.5  # High GC overhead
        
        ops_per_hour = (telemetry.read_ops + telemetry.write_ops) / 24
        predicted_lifetime = self.wear_model.predict_block_lifetime(
            int(avg_wear * 1.05), int(ops_per_hour)
        )
        
        return PredictedState(
            timestamp=time.time(),
            predicted_wear=predicted_wear,
            predicted_latency=predicted_latency,
            predicted_errors=telemetry.error_count,
            predicted_lifetime_hours=predicted_lifetime,
            confidence=0.75
        )
    
    def _simulate_no_action(self, telemetry) -> PredictedState:
        """Simulate taking no action (baseline)"""
        avg_wear = sum(telemetry.wear_counters.values()) / max(len(telemetry.wear_counters), 1)
        predicted_wear = {
            block_id: wear
            for block_id, wear in list(telemetry.wear_counters.items())[:10]
        }
        
        queue_depth = self.latency_model.predict_queue_congestion(
            telemetry.read_ops + telemetry.write_ops, 1000
        )
        predicted_latency = self.latency_model.predict_write_latency(
            telemetry.io_workload, queue_depth, avg_wear / 10000
        )
        
        ops_per_hour = (telemetry.read_ops + telemetry.write_ops) / 24
        predicted_lifetime = self.wear_model.predict_block_lifetime(
            int(avg_wear), int(ops_per_hour)
        )
        
        return PredictedState(
            timestamp=time.time(),
            predicted_wear=predicted_wear,
            predicted_latency=predicted_latency,
            predicted_errors=telemetry.error_count,
            predicted_lifetime_hours=predicted_lifetime,
            confidence=0.95
        )
    
    def get_prediction_history(self, count: int = 10) -> List[PredictedState]:
        """Get recent prediction history"""
        return self.prediction_history[-count:]
