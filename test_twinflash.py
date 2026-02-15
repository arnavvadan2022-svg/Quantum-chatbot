#!/usr/bin/env python3
"""
TwinFlash AI - Demo and Test Script
Demonstrates the complete TwinFlash architecture in action
"""

import sys
import json
from src.twinflash import TwinFlashSystem


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_architecture():
    """Demonstrate TwinFlash architecture"""
    print_section("TWINFLASH AI - ARCHITECTURE DEMO")
    
    # Initialize system
    twinflash = TwinFlashSystem(capacity_gb=256, num_blocks=1000)
    
    # Show architecture info
    print_section("ARCHITECTURE INFORMATION")
    architecture = twinflash.get_architecture_info()
    
    print("\n📐 System Layers:")
    for i, layer in enumerate(architecture['layers'], 1):
        print(f"\n{i}. {layer['name']}")
        print(f"   Role: {layer['role']}")
        print(f"   Provides: {layer['provides']}")
        
        if 'components' in layer:
            print(f"   Components: {', '.join(layer['components'])}")
        if 'techniques' in layer:
            print(f"   Techniques: {', '.join(layer['techniques'])}")
        if 'models' in layer:
            print(f"   Models: {', '.join(layer['models'])}")
    
    print("\n\n📊 Data Flow Pipeline:")
    for step in architecture['data_flow']:
        print(f"   {step}")
    
    # Show explanation
    print_section("ARCHITECTURE EXPLANATION")
    print(twinflash.explain_architecture())
    
    return twinflash


def demo_single_lifecycle(twinflash):
    """Demonstrate a single lifecycle"""
    print_section("SINGLE LIFECYCLE DEMO")
    
    result = twinflash.run_lifecycle(simulate_workload=True)
    
    print("\n📊 Lifecycle Result:")
    print(f"   Action Taken: {result['action_taken']}")
    print(f"   Description: {result['action_description']}")
    print(f"   Execution Status: {result['execution_result']['status']}")
    print(f"   SSD Health Score: {result['ssd_health']:.2f}")
    
    print("\n🎯 Predicted vs Actual Metrics:")
    predicted = result['predicted_metrics']
    actual = result['actual_metrics']
    
    print(f"   Wear:     {predicted.get('wear', 0):.3f} (predicted)")
    print(f"   Latency:  {predicted.get('latency', 0):.3f} (predicted)")
    print(f"   Lifetime: {predicted.get('lifetime', 0):.3f} (predicted)")
    
    print("\n📈 Feedback:")
    feedback = result['feedback']
    print(f"   Prediction Accurate: {feedback['prediction_accurate']}")
    print(f"   Total Error: {feedback['total_error']:.3f}")


def demo_continuous_operation(twinflash):
    """Demonstrate continuous operation"""
    print_section("CONTINUOUS OPERATION DEMO")
    
    print("\n🔄 Running 5 continuous lifecycles...\n")
    results = twinflash.run_continuous(num_cycles=5)
    
    print("\n📊 Summary of Results:")
    print(f"   Total Cycles: {len(results)}")
    
    # Analyze actions taken
    actions_taken = {}
    for result in results:
        action = result['action_taken']
        actions_taken[action] = actions_taken.get(action, 0) + 1
    
    print("\n   Actions Taken:")
    for action, count in actions_taken.items():
        print(f"     • {action}: {count} times")
    
    # Show health trend
    print("\n   SSD Health Trend:")
    for i, result in enumerate(results, 1):
        health = result['ssd_health']
        bar = "█" * int(health * 20)
        print(f"     Cycle {i}: {bar} {health:.2f}")
    
    # Average accuracy
    accurate_count = sum(1 for r in results if r['feedback']['prediction_accurate'])
    accuracy_rate = accurate_count / len(results)
    print(f"\n   Prediction Accuracy: {accuracy_rate:.1%}")


def demo_system_status(twinflash):
    """Show system status"""
    print_section("SYSTEM STATUS")
    
    status = twinflash.get_system_status()
    
    print("\n📊 SSD Statistics:")
    ssd = status['ssd']
    print(f"   Total Operations: {ssd['total_operations']}")
    print(f"   Read Ops: {ssd['read_ops']}")
    print(f"   Write Ops: {ssd['write_ops']}")
    print(f"   Error Count: {ssd['error_count']}")
    print(f"   Temperature: {ssd['temperature_celsius']}°C")
    print(f"   Average Wear: {ssd['average_wear']}")
    
    print("\n   Block Status:")
    blocks = ssd['blocks']
    print(f"     Total: {blocks['total']}")
    print(f"     Free:  {blocks['free']}")
    print(f"     Used:  {blocks['used']}")
    print(f"     Bad:   {blocks['bad']}")
    
    print("\n   Capacity:")
    capacity = ssd['capacity']
    print(f"     Total: {capacity['total_gb']} GB")
    print(f"     Used:  {capacity['used_gb']} GB")
    print(f"     Free:  {capacity['free_gb']} GB")
    
    print("\n🧠 RL Engine Statistics:")
    rl = status['rl_engine']
    print(f"   Decisions Made: {rl['decision_count']}")
    
    policy = rl['policy_stats']
    print(f"   Training Steps: {policy['training_steps']}")
    print(f"   Average Reward: {policy['avg_reward']}")
    print(f"   Exploration Rate: {policy['exploration_rate']:.3f}")
    
    print("\n⚡ Executor Statistics:")
    executor = status['executor']
    print(f"   Executed Actions: {executor['total_executed']}")
    print(f"   Blocked Actions: {executor['total_blocked']}")
    print(f"   Success Rate: {executor['success_rate']:.1%}")
    
    print("\n📚 Learning Statistics:")
    learning = status['learning']
    print(f"   Total Predictions: {learning['total_predictions']}")
    print(f"   Accurate Predictions: {learning['accurate_predictions']}")
    print(f"   Accuracy Rate: {learning['accuracy_rate']:.1%}")
    print(f"   Average Error: {learning['average_error']:.3f}")
    
    if 'improvement_percentage' in learning['improvement']:
        improvement = learning['improvement']
        print(f"\n   Model Improvement: {improvement['improvement_percentage']:.1f}%")
        print(f"   {improvement['message']}")


def main():
    """Main demo function"""
    print("\n" + "=" * 70)
    print("🚀 TWINFLASH AI - COMPREHENSIVE DEMONSTRATION")
    print("=" * 70)
    print("\nThis demo showcases the complete TwinFlash AI architecture")
    print("for intelligent SSD management using Digital Twin technology")
    print("and Reinforcement Learning.\n")
    
    try:
        # Demo 1: Architecture
        twinflash = demo_architecture()
        
        # Demo 2: Single lifecycle
        demo_single_lifecycle(twinflash)
        
        # Demo 3: Continuous operation
        demo_continuous_operation(twinflash)
        
        # Demo 4: System status
        demo_system_status(twinflash)
        
        print_section("DEMO COMPLETE")
        print("\n✅ All demonstrations completed successfully!")
        print("\n💡 Key Takeaways:")
        print("   • TwinFlash creates a digital twin of physical SSD")
        print("   • RL engine simulates multiple futures and selects optimal action")
        print("   • System learns from outcomes via continuous feedback")
        print("   • Safety mechanisms prevent risky decisions")
        print("   • Architecture is modular and scalable")
        
        print("\n🔗 API Endpoints Available:")
        print("   • GET  /api/twinflash/status - System status")
        print("   • GET  /api/twinflash/architecture - Architecture info")
        print("   • POST /api/twinflash/run-lifecycle - Run single cycle")
        print("   • POST /api/twinflash/run-continuous - Run multiple cycles")
        print("   • GET  /api/twinflash/ssd-stats - SSD statistics")
        
        print("\n" + "=" * 70)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
