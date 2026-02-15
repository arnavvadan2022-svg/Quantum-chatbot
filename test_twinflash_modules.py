#!/usr/bin/env python3
"""
Simple TwinFlash module test
Tests that all TwinFlash modules can be imported and initialized
"""

import sys

def test_imports():
    """Test that all modules can be imported"""
    print("Testing TwinFlash module imports...")
    
    try:
        from src.twinflash.ssd_layer import RealSSDLayer
        print("  ✓ ssd_layer imported")
        
        from src.twinflash.state_sync import StateSynchronizer
        print("  ✓ state_sync imported")
        
        from src.twinflash.digital_twin import DigitalTwin
        print("  ✓ digital_twin imported")
        
        from src.twinflash.rl_engine import CounterfactualRLEngine
        print("  ✓ rl_engine imported")
        
        from src.twinflash.decision_executor import DecisionExecutor
        print("  ✓ decision_executor imported")
        
        from src.twinflash.feedback_logger import FeedbackLogger
        print("  ✓ feedback_logger imported")
        
        from src.twinflash.twinflash_core import TwinFlashSystem
        print("  ✓ twinflash_core imported")
        
        print("\n✅ All modules imported successfully!\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_initialization():
    """Test that TwinFlash can be initialized"""
    print("Testing TwinFlash initialization...")
    
    try:
        from src.twinflash import TwinFlashSystem
        
        # Initialize with small parameters for quick test
        twinflash = TwinFlashSystem(capacity_gb=256, num_blocks=1000)
        
        print("\n✅ TwinFlash initialized successfully!\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Initialization error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_basic_operation():
    """Test basic TwinFlash operation"""
    print("Testing basic TwinFlash operation...")
    
    try:
        from src.twinflash import TwinFlashSystem
        
        twinflash = TwinFlashSystem(capacity_gb=256, num_blocks=1000)
        
        # Test getting status
        status = twinflash.get_system_status()
        print(f"  System status: {status['system']['status']}")
        
        # Test architecture info
        architecture = twinflash.get_architecture_info()
        print(f"  Architecture: {architecture['architecture']}")
        print(f"  Layers: {len(architecture['layers'])}")
        
        print("\n✅ Basic operations work correctly!\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Operation error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 70)
    print("TWINFLASH AI - MODULE TESTS")
    print("=" * 70)
    print()
    
    results = []
    
    # Test 1: Imports
    results.append(("Imports", test_imports()))
    
    # Test 2: Initialization
    results.append(("Initialization", test_initialization()))
    
    # Test 3: Basic Operations
    results.append(("Basic Operations", test_basic_operation()))
    
    # Summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 70)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
