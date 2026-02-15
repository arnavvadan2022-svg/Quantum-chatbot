"""
Counterfactual RL Layer (Decision Engine)
Brain of the system - runs multiple parallel futures and selects best action
"""

import time
from typing import Dict, List, Tuple
from dataclasses import dataclass
from .digital_twin import DigitalTwin, PredictedState


@dataclass
class Action:
    """Action that can be taken on SSD"""
    name: str
    parameters: Dict
    description: str


@dataclass
class FutureScenario:
    """A possible future outcome"""
    action: Action
    predicted_state: PredictedState
    metrics: Dict[str, float]
    score: float


class ActionGenerator:
    """
    Generates possible actions for the system to consider
    """
    
    def __init__(self):
        self.available_actions = [
            'compress_now',
            'delay_compress',
            'migrate_block',
            'reallocate',
            'gc_trigger'
        ]
    
    def generate_actions(self, current_state) -> List[Action]:
        """
        Generate set of possible actions A = {a1, a2, ..., an}
        """
        actions = []
        
        # Action 1: Compress now
        actions.append(Action(
            name='compress_now',
            parameters={'compression_level': 6},
            description='Apply data compression immediately to reduce write amplification'
        ))
        
        # Action 2: Delay compression
        actions.append(Action(
            name='delay_compress',
            parameters={'delay_hours': 4},
            description='Postpone compression to avoid performance overhead during peak usage'
        ))
        
        # Action 3: Migrate blocks
        actions.append(Action(
            name='migrate_block',
            parameters={'target_blocks': 'low_wear'},
            description='Move data from high-wear blocks to healthier blocks'
        ))
        
        # Action 4: Reallocate
        actions.append(Action(
            name='reallocate',
            parameters={'strategy': 'wear_leveling'},
            description='Redistribute data across blocks for even wear distribution'
        ))
        
        # Action 5: Trigger GC
        actions.append(Action(
            name='gc_trigger',
            parameters={'aggressive': False},
            description='Run garbage collection to reclaim free space'
        ))
        
        return actions


class ParallelSimulator:
    """
    Parallel Simulation Engine
    For each action, creates Future_i = Twin(S(t), A_i)
    """
    
    def __init__(self, digital_twin: DigitalTwin):
        self.twin = digital_twin
    
    def simulate_futures(self, actions: List[Action]) -> List[Tuple[Action, PredictedState]]:
        """
        Simulate multiple parallel futures for all actions
        Creates counterfactual scenarios: "What if we do X?"
        """
        futures = []
        
        print(f"[ParallelSimulator] Simulating {len(actions)} parallel futures...")
        
        for action in actions:
            # Simulate this action's outcome
            predicted_state = self.twin.simulate_action(
                action.name,
                action.parameters
            )
            
            futures.append((action, predicted_state))
            print(f"  • {action.name}: confidence={predicted_state.confidence}")
        
        return futures


class EvaluationEngine:
    """
    Evaluation Engine
    Measures: Wear, Latency, Error, Lifetime, Energy
    """
    
    def __init__(self):
        # Metric weights (can be tuned)
        self.weights = {
            'wear': 0.30,      # Minimize wear damage
            'latency': 0.25,   # Minimize delay
            'error': 0.20,     # Minimize errors
            'lifetime': 0.20,  # Maximize lifetime
            'energy': 0.05     # Minimize power consumption
        }
    
    def evaluate_future(self, action: Action, predicted_state: PredictedState) -> Dict[str, float]:
        """
        Evaluate a future scenario across multiple metrics
        Returns normalized scores (0.0 to 1.0, higher is better)
        """
        metrics = {}
        
        # Metric 1: Wear (lower is better, so invert)
        avg_predicted_wear = sum(predicted_state.predicted_wear.values()) / max(len(predicted_state.predicted_wear), 1)
        wear_score = max(0.0, 1.0 - (avg_predicted_wear / 10000.0))
        metrics['wear'] = wear_score
        
        # Metric 2: Latency (lower is better, so invert)
        # Normalize latency to 0-1 range (assuming max 5ms)
        latency_score = max(0.0, 1.0 - (predicted_state.predicted_latency / 5.0))
        metrics['latency'] = latency_score
        
        # Metric 3: Error (lower is better, so invert)
        # Normalize error count (assuming max 1000 errors)
        error_score = max(0.0, 1.0 - (predicted_state.predicted_errors / 1000.0))
        metrics['error'] = error_score
        
        # Metric 4: Lifetime (higher is better)
        # Normalize to 0-1 range (assuming max 10000 hours)
        lifetime_score = min(1.0, predicted_state.predicted_lifetime_hours / 10000.0)
        metrics['lifetime'] = lifetime_score
        
        # Metric 5: Energy (estimate based on action type)
        energy_score = self._estimate_energy_efficiency(action.name)
        metrics['energy'] = energy_score
        
        return metrics
    
    def _estimate_energy_efficiency(self, action_name: str) -> float:
        """Estimate energy efficiency of action (0.0 to 1.0, higher is better)"""
        energy_costs = {
            'compress_now': 0.7,      # Moderate CPU cost
            'delay_compress': 0.95,   # Very low cost (delay)
            'migrate_block': 0.6,     # High I/O cost
            'reallocate': 0.7,        # Moderate cost
            'gc_trigger': 0.5         # High cost
        }
        return energy_costs.get(action_name, 0.8)
    
    def calculate_score(self, metrics: Dict[str, float]) -> float:
        """
        Calculate overall score using weighted metrics
        Returns: 0.0 to 1.0 (higher is better)
        """
        score = sum(
            metrics[metric] * self.weights[metric]
            for metric in self.weights.keys()
        )
        return round(score, 3)


class RLPolicyNetwork:
    """
    RL Policy Network
    Learns optimal policy: π(S) → A*
    
    Uses: DQN / PPO
    Reward shaping
    Constraint handling
    """
    
    def __init__(self):
        # Policy parameters (simplified - in real system would be neural network)
        self.policy_params = {
            'exploration_rate': 0.1,  # 10% random exploration
            'learning_rate': 0.001,
            'discount_factor': 0.95
        }
        
        # Experience replay buffer
        self.experience_buffer = []
        self.max_buffer_size = 1000
        
        # Training statistics
        self.training_steps = 0
        self.total_reward = 0.0
    
    def select_action(self, state, evaluated_futures: List[FutureScenario]) -> Action:
        """
        Select best action using learned policy
        π(S) → A*
        """
        # Exploration vs exploitation
        if self._should_explore():
            # Explore: random action
            import random
            return random.choice(evaluated_futures).action
        else:
            # Exploit: best action based on scores
            best_future = max(evaluated_futures, key=lambda f: f.score)
            return best_future.action
    
    def _should_explore(self) -> bool:
        """Decide whether to explore or exploit"""
        import random
        return random.random() < self.policy_params['exploration_rate']
    
    def update_policy(self, state, action: Action, reward: float, next_state):
        """
        Update policy based on experience
        This is where learning happens
        """
        # Store experience
        experience = {
            'state': state,
            'action': action.name,
            'reward': reward,
            'next_state': next_state,
            'timestamp': time.time()
        }
        
        self._add_experience(experience)
        
        # Update statistics
        self.training_steps += 1
        self.total_reward += reward
        
        # In a real system, this would update neural network weights
        # For now, we simulate learning by adjusting exploration rate
        if self.training_steps % 100 == 0:
            # Decay exploration rate over time
            self.policy_params['exploration_rate'] *= 0.99
            self.policy_params['exploration_rate'] = max(0.01, self.policy_params['exploration_rate'])
    
    def _add_experience(self, experience: Dict):
        """Add experience to replay buffer"""
        self.experience_buffer.append(experience)
        
        # Keep buffer size limited
        if len(self.experience_buffer) > self.max_buffer_size:
            self.experience_buffer = self.experience_buffer[-self.max_buffer_size:]
    
    def get_policy_stats(self) -> Dict:
        """Get policy statistics"""
        return {
            'training_steps': self.training_steps,
            'total_reward': round(self.total_reward, 2),
            'avg_reward': round(self.total_reward / max(self.training_steps, 1), 3),
            'exploration_rate': self.policy_params['exploration_rate'],
            'experience_buffer_size': len(self.experience_buffer)
        }


class CounterfactualRLEngine:
    """
    Counterfactual RL Layer - Decision Engine
    
    Role: Brain of the system. Runs multiple "parallel futures"
    Components:
    - Action Generator: Generates possible actions
    - Parallel Simulation Engine: Simulates each action's outcome
    - Evaluation Engine: Scores each outcome
    - RL Policy Network: Learns and selects optimal action
    
    Output: Optimal Action A*
    """
    
    def __init__(self, digital_twin: DigitalTwin):
        self.action_generator = ActionGenerator()
        self.parallel_simulator = ParallelSimulator(digital_twin)
        self.evaluation_engine = EvaluationEngine()
        self.policy_network = RLPolicyNetwork()
        
        self.decision_count = 0
        
        print("[CounterfactualRL] Decision engine initialized")
    
    def make_decision(self, current_state) -> Tuple[Action, List[FutureScenario]]:
        """
        Main decision-making pipeline
        
        1. Generate actions
        2. Simulate parallel futures
        3. Evaluate each future
        4. Select optimal action
        
        Returns: (optimal_action, all_evaluated_futures)
        """
        print(f"\n[CounterfactualRL] Making decision #{self.decision_count + 1}")
        
        # Step 1: Generate possible actions
        actions = self.action_generator.generate_actions(current_state)
        print(f"  1. Generated {len(actions)} possible actions")
        
        # Step 2: Simulate parallel futures
        futures = self.parallel_simulator.simulate_futures(actions)
        print(f"  2. Simulated {len(futures)} parallel futures")
        
        # Step 3: Evaluate each future
        evaluated_futures = []
        print("  3. Evaluating futures:")
        
        for action, predicted_state in futures:
            metrics = self.evaluation_engine.evaluate_future(action, predicted_state)
            score = self.evaluation_engine.calculate_score(metrics)
            
            scenario = FutureScenario(
                action=action,
                predicted_state=predicted_state,
                metrics=metrics,
                score=score
            )
            evaluated_futures.append(scenario)
            
            print(f"     • {action.name}: score={score:.3f} (wear={metrics['wear']:.2f}, "
                  f"latency={metrics['latency']:.2f}, lifetime={metrics['lifetime']:.2f})")
        
        # Step 4: Select optimal action using RL policy
        optimal_action = self.policy_network.select_action(current_state, evaluated_futures)
        print(f"  4. Selected optimal action: {optimal_action.name}")
        
        self.decision_count += 1
        
        return optimal_action, evaluated_futures
    
    def learn_from_outcome(self, state, action: Action, actual_outcome: Dict):
        """
        Learn from actual outcome (feedback loop)
        """
        # Calculate reward based on actual outcome
        reward = self._calculate_reward(actual_outcome)
        
        # Update policy
        self.policy_network.update_policy(state, action, reward, actual_outcome)
        
        print(f"[CounterfactualRL] Learned from outcome: reward={reward:.2f}")
    
    def _calculate_reward(self, outcome: Dict) -> float:
        """Calculate reward from actual outcome"""
        # Reward is based on how well the action performed
        # Higher reward for better outcomes
        
        # Example: reward based on health improvement
        health_score = outcome.get('health_score', 0.5)
        error_count = outcome.get('error_count', 0)
        
        reward = health_score * 10.0  # Scale to reasonable range
        reward -= error_count * 0.1   # Penalty for errors
        
        return reward
    
    def get_statistics(self) -> Dict:
        """Get engine statistics"""
        return {
            'decision_count': self.decision_count,
            'policy_stats': self.policy_network.get_policy_stats()
        }
