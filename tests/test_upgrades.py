"""
Tests for upgrade system
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.resources import ResourceManager
from src.upgrades import Upgrade, UpgradeTree

def test_upgrade_initialization():
    """Test upgrade creation"""
    upgrade = Upgrade(
        "test", "Test Upgrade", "Test description",
        {"iron": 100}, "mining_power", 5
    )
    
    assert upgrade.id == "test"
    assert upgrade.level == 0
    assert upgrade.unlocked == True

def test_upgrade_cost_scaling():
    """Test upgrade cost increases with levels"""
    upgrade = Upgrade(
        "test", "Test", "Test",
        {"iron": 100}, "mining_power", 5,
        cost_scaling=1.5
    )
    
    cost1 = upgrade.get_cost()
    assert cost1["iron"] == 100
    
    upgrade.level = 1
    cost2 = upgrade.get_cost()
    assert cost2["iron"] == 150  # 100 * 1.5^1
    
    upgrade.level = 2
    cost3 = upgrade.get_cost()
    assert cost3["iron"] == 225  # 100 * 1.5^2

def test_upgrade_purchase():
    """Test purchasing upgrades"""
    rm = ResourceManager()
    rm.add("iron", 500)
    
    upgrade = Upgrade(
        "test", "Test", "Test",
        {"iron": 100}, "mining_power", 5
    )
    
    # First purchase
    assert upgrade.purchase(rm) == True
    assert upgrade.level == 1
    assert rm.get("iron") == 400
    
    # Second purchase (costs more - 100 * 1.5 = 150)
    assert upgrade.purchase(rm) == True
    assert upgrade.level == 2
    assert rm.get("iron") == 250

def test_upgrade_max_level():
    """Test max level constraint"""
    rm = ResourceManager()
    rm.add("iron", 10000)
    
    upgrade = Upgrade(
        "test", "Test", "Test",
        {"iron": 100}, "mining_power", 5,
        max_level=3
    )
    
    # Buy to max level
    upgrade.purchase(rm)
    upgrade.purchase(rm)
    upgrade.purchase(rm)
    
    assert upgrade.level == 3
    assert upgrade.get_cost() == None
    assert upgrade.purchase(rm) == False

def test_upgrade_prerequisites():
    """Test prerequisite system"""
    upgrade1 = Upgrade("prereq", "Prereq", "Test", {"iron": 10}, "test", 1)
    upgrade2 = Upgrade("main", "Main", "Test", {"iron": 20}, "test", 1, 
                      prerequisites=["prereq"])
    
    assert upgrade1.unlocked == True
    assert upgrade2.unlocked == False

def test_upgrade_tree():
    """Test upgrade tree management"""
    rm = ResourceManager()
    rm.add("iron", 1000)
    
    tree = UpgradeTree(rm)
    
    # Verify we have 50+ upgrades
    assert len(tree.upgrades) >= 50
    
    # Test purchasing an upgrade
    assert tree.purchase_upgrade("mining_power_1") == True
    assert tree.get_upgrade("mining_power_1").level == 1

def test_upgrade_effects():
    """Test calculating total effects"""
    rm = ResourceManager()
    rm.add("iron", 10000)
    
    tree = UpgradeTree(rm)
    
    # Purchase multiple power upgrades
    tree.purchase_upgrade("mining_power_1")
    tree.purchase_upgrade("power_boost_1")
    
    # Get total mining power effect
    total_power = tree.get_total_effect("mining_power")
    assert total_power > 0

if __name__ == "__main__":
    test_upgrade_initialization()
    test_upgrade_cost_scaling()
    test_upgrade_purchase()
    test_upgrade_max_level()
    test_upgrade_prerequisites()
    test_upgrade_tree()
    test_upgrade_effects()
    print("All upgrade tests passed!")
