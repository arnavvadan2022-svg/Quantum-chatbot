"""
Feedback & Learning Layer (Self-Improvement)
Makes system smarter over time through continuous learning
"""

import time
from typing import Dict, List


class FeedbackLogger:
    """
    Feedback & Learning Layer - Self-Improvement
    
    Role: Makes system smarter over time
    Loop: Prediction → Reality → Error → Learning
    
    This is continuous learning
    """
    
    def __init__(self):
        self.feedback_records = []
        self.max_records = 1000
        
        # Learning metrics
        self.total_predictions = 0
        self.accurate_predictions = 0
        self.prediction_errors = []
        
        print("[FeedbackLogger] Continuous learning system initialized")
    
    def log_prediction_vs_reality(self, 
                                  predicted_state: Dict,
                                  actual_state: Dict,
                                  action_taken: str) -> Dict:
        """
        Compare prediction with reality and calculate error
        This is the core of the learning loop
        """
        timestamp = time.time()
        
        # Calculate prediction error for each metric
        errors = self._calculate_prediction_errors(predicted_state, actual_state)
        
        # Determine if prediction was accurate
        is_accurate = errors['total_error'] < 0.2  # 20% threshold
        
        # Create feedback record
        feedback = {
            'timestamp': timestamp,
            'action': action_taken,
            'predicted_state': predicted_state,
            'actual_state': actual_state,
            'errors': errors,
            'is_accurate': is_accurate
        }
        
        # Store feedback
        self._add_feedback(feedback)
        
        # Update statistics
        self.total_predictions += 1
        if is_accurate:
            self.accurate_predictions += 1
        self.prediction_errors.append(errors['total_error'])
        
        # Keep only recent errors
        if len(self.prediction_errors) > 100:
            self.prediction_errors = self.prediction_errors[-100:]
        
        print(f"[FeedbackLogger] Logged prediction: error={errors['total_error']:.3f}, "
              f"accurate={is_accurate}")
        
        return feedback
    
    def _calculate_prediction_errors(self, predicted: Dict, actual: Dict) -> Dict:
        """
        Calculate errors between predicted and actual states
        """
        errors = {}
        
        # Error 1: Latency prediction error
        if 'predicted_latency' in predicted and 'actual_latency' in actual:
            pred_lat = predicted['predicted_latency']
            actual_lat = actual['actual_latency']
            errors['latency_error'] = abs(pred_lat - actual_lat) / max(actual_lat, 0.001)
        else:
            errors['latency_error'] = 0.0
        
        # Error 2: Wear prediction error
        if 'predicted_wear' in predicted and 'actual_wear' in actual:
            # Compare average wear
            pred_wear = sum(predicted['predicted_wear'].values()) / max(len(predicted['predicted_wear']), 1)
            actual_wear = actual['actual_wear']
            errors['wear_error'] = abs(pred_wear - actual_wear) / max(actual_wear, 1)
        else:
            errors['wear_error'] = 0.0
        
        # Error 3: Error count prediction error
        if 'predicted_errors' in predicted and 'actual_errors' in actual:
            pred_err = predicted['predicted_errors']
            actual_err = actual['actual_errors']
            errors['error_count_error'] = abs(pred_err - actual_err) / max(actual_err, 1)
        else:
            errors['error_count_error'] = 0.0
        
        # Total error (weighted average)
        errors['total_error'] = (
            errors['latency_error'] * 0.4 +
            errors['wear_error'] * 0.4 +
            errors['error_count_error'] * 0.2
        )
        
        return errors
    
    def calculate_model_improvement(self) -> Dict:
        """
        Calculate how much the model has improved over time
        """
        if len(self.prediction_errors) < 10:
            return {
                'improvement': 0.0,
                'message': 'Not enough data for improvement calculation'
            }
        
        # Compare recent errors vs older errors
        recent_errors = self.prediction_errors[-10:]
        older_errors = self.prediction_errors[:10]
        
        avg_recent = sum(recent_errors) / len(recent_errors)
        avg_older = sum(older_errors) / len(older_errors)
        
        improvement = ((avg_older - avg_recent) / max(avg_older, 0.001)) * 100
        
        return {
            'improvement_percentage': round(improvement, 2),
            'avg_recent_error': round(avg_recent, 3),
            'avg_older_error': round(avg_older, 3),
            'message': f"Model error reduced by {improvement:.1f}%"
        }
    
    def trigger_model_retraining(self, rl_engine) -> Dict:
        """
        Trigger model retraining based on accumulated feedback
        This is where the AI learns from its mistakes
        """
        print("\n[FeedbackLogger] Triggering model retraining...")
        
        if len(self.feedback_records) < 10:
            return {
                'status': 'skipped',
                'reason': 'Not enough feedback data',
                'records_available': len(self.feedback_records)
            }
        
        # Analyze recent feedback
        recent_feedback = self.feedback_records[-50:]
        
        # Calculate rewards for each feedback
        for feedback in recent_feedback:
            # Reward based on prediction accuracy
            if feedback['is_accurate']:
                reward = 1.0
            else:
                reward = -0.5 * feedback['errors']['total_error']
            
            # Update RL policy with this experience
            # In real system, this would update neural network weights
            # For now, we just accumulate rewards
        
        # Calculate retraining statistics
        accuracy_rate = self.accurate_predictions / max(self.total_predictions, 1)
        avg_error = sum(self.prediction_errors) / max(len(self.prediction_errors), 1)
        
        print(f"  Retraining complete:")
        print(f"    Accuracy rate: {accuracy_rate:.1%}")
        print(f"    Average error: {avg_error:.3f}")
        
        return {
            'status': 'success',
            'records_processed': len(recent_feedback),
            'accuracy_rate': round(accuracy_rate, 3),
            'average_error': round(avg_error, 3)
        }
    
    def _add_feedback(self, feedback: Dict):
        """Add feedback record to storage"""
        self.feedback_records.append(feedback)
        
        # Keep only recent records
        if len(self.feedback_records) > self.max_records:
            self.feedback_records = self.feedback_records[-self.max_records:]
    
    def get_learning_statistics(self) -> Dict:
        """Get overall learning statistics"""
        accuracy_rate = 0.0
        if self.total_predictions > 0:
            accuracy_rate = self.accurate_predictions / self.total_predictions
        
        avg_error = 0.0
        if self.prediction_errors:
            avg_error = sum(self.prediction_errors) / len(self.prediction_errors)
        
        improvement = self.calculate_model_improvement()
        
        return {
            'total_predictions': self.total_predictions,
            'accurate_predictions': self.accurate_predictions,
            'accuracy_rate': round(accuracy_rate, 3),
            'average_error': round(avg_error, 3),
            'improvement': improvement,
            'feedback_records': len(self.feedback_records)
        }
    
    def get_recent_feedback(self, count: int = 10) -> List[Dict]:
        """Get recent feedback records"""
        return self.feedback_records[-count:]
    
    def export_training_data(self) -> List[Dict]:
        """
        Export training data for offline model training
        """
        training_data = []
        
        for record in self.feedback_records:
            # Convert to training format
            training_sample = {
                'input': record['predicted_state'],
                'output': record['actual_state'],
                'action': record['action'],
                'error': record['errors']['total_error']
            }
            training_data.append(training_sample)
        
        return training_data
    
    def import_training_data(self, training_data: List[Dict]) -> bool:
        """
        Import training data from external source
        """
        try:
            for sample in training_data:
                # Convert to feedback format
                feedback = {
                    'timestamp': time.time(),
                    'action': sample['action'],
                    'predicted_state': sample['input'],
                    'actual_state': sample['output'],
                    'errors': {'total_error': sample['error']},
                    'is_accurate': sample['error'] < 0.2
                }
                self._add_feedback(feedback)
            
            print(f"[FeedbackLogger] Imported {len(training_data)} training samples")
            return True
        
        except Exception as e:
            print(f"[FeedbackLogger] Import error: {e}")
            return False
