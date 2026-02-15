"""
TwinFlash AI - Core System
Orchestrates all layers in the pipeline
"""

import time
from typing import Dict, Optional, List
from .ssd_layer import RealSSDLayer
from .state_sync import StateSynchronizer
from .digital_twin import DigitalTwin
from .rl_engine import CounterfactualRLEngine
from .decision_executor import DecisionExecutor
from .feedback_logger import FeedbackLogger


class TwinFlashSystem:
    """
    TwinFlash AI - Complete System
    
    Architecture Pipeline:
    Input → Twin → Simulation → Intelligence → Execution → Feedback
    
    5 Main Layers:
    1. Real SSD Layer (Physical)
    2. State Synchronization
    3. Digital Twin (Simulation)
    4. Counterfactual RL (Decision)
    5. Decision Execution
    6. Feedback & Learning
    """
    
    def __init__(self, capacity_gb: int = 256, num_blocks: int = 1000):
        print("=" * 70)
        print("🚀 TWINFLASH AI - INITIALIZING")
        print("=" * 70)
        
        # Layer 1: Real SSD Layer
        print("\n[1/6] Initializing Real SSD Layer...")
        self.ssd_layer = RealSSDLayer(capacity_gb, num_blocks)
        
        # Layer 2: State Synchronization
        print("[2/6] Initializing State Synchronization Layer...")
        self.state_sync = StateSynchronizer(sync_interval=1.0)
        
        # Layer 3: Digital Twin
        print("[3/6] Initializing Digital Twin Layer...")
        self.digital_twin = DigitalTwin()
        
        # Layer 4: Counterfactual RL Engine
        print("[4/6] Initializing Counterfactual RL Engine...")
        self.rl_engine = CounterfactualRLEngine(self.digital_twin)
        
        # Layer 5: Decision Executor
        print("[5/6] Initializing Decision Executor...")
        self.executor = DecisionExecutor(self.ssd_layer, safety_threshold=0.7)
        
        # Layer 6: Feedback Logger
        print("[6/6] Initializing Feedback Logger...")
        self.feedback_logger = FeedbackLogger()
        
        # System state
        self.running = False
        self.lifecycle_count = 0
        
        print("\n" + "=" * 70)
        print("✅ TWINFLASH AI - READY")
        print("=" * 70)
    
    def run_lifecycle(self, simulate_workload: bool = True) -> Dict:
        """
        Run complete TwinFlash lifecycle
        
        Complete Lifecycle:
        1. User writes file (or simulated workload)
        2. SSD updates state
        3. Twin syncs
        4. AI generates actions
        5. Twin simulates futures
        6. AI evaluates
        7. Best action selected
        8. Real SSD executes
        9. Result logged
        10. Model retrained
        
        Returns: lifecycle result with all metrics
        """
        self.lifecycle_count += 1
        
        print("\n" + "=" * 70)
        print(f"🔄 LIFECYCLE #{self.lifecycle_count}")
        print("=" * 70)
        
        # Step 1-2: Simulate user workload
        if simulate_workload:
            print("\n[Step 1-2] Simulating user workload...")
            self.ssd_layer.simulate_workload(num_operations=50)
        
        # Step 3: Get telemetry and sync state
        print("\n[Step 3] Syncing state from real SSD...")
        telemetry = self.ssd_layer.get_telemetry()
        current_state = self.state_sync.sync_state(telemetry)
        
        # Update digital twin
        self.digital_twin.sync_from_real(current_state)
        
        print(f"  State synced: health_score={current_state.metadata['health_score']:.2f}, "
              f"workload={telemetry.io_workload:.2f}")
        
        # Step 4-7: AI makes decision
        print("\n[Step 4-7] AI decision-making process...")
        optimal_action, all_futures = self.rl_engine.make_decision(current_state)
        
        # Get best future scenario
        best_future = max(all_futures, key=lambda f: f.score)
        
        # Step 8: Execute decision on real SSD
        print("\n[Step 8] Executing decision on real SSD...")
        execution_result = self.executor.execute(
            optimal_action,
            best_future.predicted_state.confidence,
            best_future.metrics
        )
        
        # Step 9: Observe actual outcome
        print("\n[Step 9] Observing actual outcome...")
        time.sleep(0.1)  # Simulate operation time
        
        actual_telemetry = self.ssd_layer.get_telemetry()
        actual_state = {
            'health_score': self.state_sync._calculate_health_score(actual_telemetry),
            'actual_latency': 0.5,  # Simulated
            'actual_wear': sum(actual_telemetry.wear_counters.values()) / len(actual_telemetry.wear_counters),
            'actual_errors': actual_telemetry.error_count
        }
        
        # Step 10: Log feedback and learn
        print("\n[Step 10] Logging feedback and learning...")
        feedback = self.feedback_logger.log_prediction_vs_reality(
            predicted_state=best_future.predicted_state.to_dict(),
            actual_state=actual_state,
            action_taken=optimal_action.name
        )
        
        # Update RL policy
        self.rl_engine.learn_from_outcome(current_state, optimal_action, actual_state)
        
        # Periodic retraining
        if self.lifecycle_count % 10 == 0:
            self.feedback_logger.trigger_model_retraining(self.rl_engine)
        
        print("\n" + "=" * 70)
        print(f"✅ LIFECYCLE #{self.lifecycle_count} COMPLETE")
        print("=" * 70)
        
        # Return comprehensive result
        return {
            'lifecycle_number': self.lifecycle_count,
            'action_taken': optimal_action.name,
            'action_description': optimal_action.description,
            'execution_result': execution_result,
            'predicted_metrics': best_future.metrics,
            'actual_metrics': actual_state,
            'feedback': {
                'prediction_accurate': feedback['is_accurate'],
                'total_error': feedback['errors']['total_error']
            },
            'ssd_health': actual_state['health_score'],
            'timestamp': time.time()
        }
    
    def run_continuous(self, num_cycles: int = 5) -> List[Dict]:
        """
        Run continuous lifecycle for multiple cycles
        Demonstrates the system running over time
        """
        print(f"\n🔁 Running {num_cycles} continuous cycles...\n")
        
        results = []
        for i in range(num_cycles):
            result = self.run_lifecycle(simulate_workload=True)
            results.append(result)
            
            # Brief pause between cycles
            time.sleep(0.5)
        
        return results
    
    def get_system_status(self) -> Dict:
        """
        Get comprehensive system status
        """
        ssd_stats = self.ssd_layer.get_statistics()
        sync_stats = self.state_sync.get_sync_statistics()
        rl_stats = self.rl_engine.get_statistics()
        executor_stats = self.executor.get_statistics()
        learning_stats = self.feedback_logger.get_learning_statistics()
        
        return {
            'system': {
                'status': 'running' if self.running else 'ready',
                'lifecycle_count': self.lifecycle_count
            },
            'ssd': ssd_stats,
            'synchronization': sync_stats,
            'rl_engine': rl_stats,
            'executor': executor_stats,
            'learning': learning_stats
        }
    
    def get_architecture_info(self) -> Dict:
        """
        Get architecture information for documentation
        """
        return {
            'architecture': 'TwinFlash AI',
            'description': 'Digital Twin Architecture for SSD Management',
            'layers': [
                {
                    'name': 'Real SSD Layer',
                    'role': 'Physical storage device interface',
                    'provides': 'Live Storage Telemetry',
                    'components': ['Read/Write Operations', 'Block Status', 'Wear Counters', 
                                  'Error Logs', 'Temperature Data', 'I/O Workload']
                },
                {
                    'name': 'State Synchronization Layer',
                    'role': 'Keep Digital Twin updated with real SSD',
                    'provides': 'S(t) = Current SSD State',
                    'techniques': ['Log Mirroring', 'Event Streaming', 'Periodic Snapshots']
                },
                {
                    'name': 'Digital Twin Layer',
                    'role': 'Virtual SSD simulation engine',
                    'provides': 'S(t+1) = Predicted State',
                    'models': ['Wear Model', 'Latency Model', 'Error Model']
                },
                {
                    'name': 'Counterfactual RL Layer',
                    'role': 'Decision engine - brain of the system',
                    'provides': 'A* = Optimal Action',
                    'components': ['Action Generator', 'Parallel Simulator', 
                                  'Evaluation Engine', 'RL Policy Network']
                },
                {
                    'name': 'Decision Executor',
                    'role': 'Execute AI decisions on real SSD',
                    'provides': 'Action Execution',
                    'safety': 'Confidence threshold + fallback rules'
                },
                {
                    'name': 'Feedback Logger',
                    'role': 'Continuous learning and self-improvement',
                    'provides': 'Model Updates',
                    'loop': 'Prediction → Reality → Error → Learning'
                }
            ],
            'data_flow': [
                'Real SSD',
                '↓',
                'State Sync',
                '↓',
                'Digital Twin',
                '↓',
                'RL Simulator',
                '↓',
                'Evaluation Engine',
                '↓',
                'Decision Unit',
                '↓',
                'Firmware Executor',
                '↓',
                'Feedback Logger',
                '↺ (Back to Twin)'
            ]
        }
    
    def explain_architecture(self) -> str:
        """
        Get human-readable architecture explanation
        """
        explanation = """
TwinFlash AI - Architecture Explanation

Our architecture mirrors the real SSD into a digital twin. This twin simulates 
multiple future scenarios for every major storage decision. A reinforcement 
learning engine evaluates these counterfactual futures using metrics like wear, 
latency, and reliability, and selects the safest action. The decision is executed 
on the real SSD and the outcome is fed back for continuous learning.

Why This Architecture Is Powerful:
✅ Systems thinking - Complete end-to-end integration
✅ AI + Hardware integration - ML models control physical device
✅ Safety mechanisms - Confidence thresholds and fallback rules
✅ Scalability awareness - Modular design for easy expansion
✅ Research depth - Based on Digital Twin and RL literature

Comparison:
┌────────────────┬─────────────────┬──────────────┐
│ Feature        │ Traditional SSD │ TwinFlash    │
├────────────────┼─────────────────┼──────────────┤
│ Decision Making│ Static          │ Adaptive     │
│ Learning       │ No              │ Yes          │
│ Simulation     │ No              │ Yes          │
│ Prediction     │ No              │ Yes          │
│ Safety         │ Limited         │ High         │
└────────────────┴─────────────────┴──────────────┘
"""
        return explanation
