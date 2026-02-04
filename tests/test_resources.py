"""
Tests for resource management system
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.resources import ResourceManager

def test_resource_initialization():
    """Test resource manager initializes correctly"""
    rm = ResourceManager()
    assert rm.get("iron") == 0
    assert rm.get("gold") == 0
    assert rm.prestige_level == 0
    assert rm.prestige_multiplier == 1.0

def test_add_resources():
    """Test adding resources"""
    rm = ResourceManager()
    rm.add("iron", 100)
    assert rm.get("iron") == 100
    rm.add("iron", 50)
    assert rm.get("iron") == 150

def test_spend_resources():
    """Test spending resources"""
    rm = ResourceManager()
    rm.add("iron", 100)
    
    # Successful spend
    assert rm.spend("iron", 50) == True
    assert rm.get("iron") == 50
    
    # Failed spend (not enough)
    assert rm.spend("iron", 100) == False
    assert rm.get("iron") == 50

def test_can_afford():
    """Test affordability checks"""
    rm = ResourceManager()
    rm.add("iron", 100)
    rm.add("gold", 50)
    
    assert rm.can_afford("iron", 50) == True
    assert rm.can_afford("iron", 150) == False
    assert rm.can_afford_multiple({"iron": 50, "gold": 25}) == True
    assert rm.can_afford_multiple({"iron": 50, "gold": 100}) == False

def test_passive_generation():
    """Test passive resource generation"""
    rm = ResourceManager()
    rm.set_passive_rate("iron", 10)  # 10 iron/sec
    
    # Simulate 1 second
    rm.update(1.0)
    assert rm.get("iron") >= 9 and rm.get("iron") <= 11  # Allow float precision

def test_prestige():
    """Test prestige reset"""
    rm = ResourceManager()
    rm.add("iron", 1000)
    rm.add("gold", 500)
    rm.add("artifact", 10)
    
    rm.prestige()
    
    # Check prestige level increased
    assert rm.prestige_level == 1
    assert rm.prestige_multiplier == 1.5
    
    # Check resources reset except artifacts
    assert rm.get("iron") == 0
    assert rm.get("gold") == 0
    assert rm.get("artifact") == 10

def test_prestige_multiplier():
    """Test prestige multiplier affects resource gain"""
    rm = ResourceManager()
    rm.prestige()  # Level 1, 1.5x multiplier
    
    rm.add("iron", 100)
    assert rm.get("iron") == 150  # 100 * 1.5

if __name__ == "__main__":
    test_resource_initialization()
    test_add_resources()
    test_spend_resources()
    test_can_afford()
    test_passive_generation()
    test_prestige()
    test_prestige_multiplier()
    print("All resource tests passed!")
