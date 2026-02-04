"""
Player character and mining mechanics
"""

import pygame
import random
import time
from .config import Config

class Player:
    """Player character"""
    
    def __init__(self, world, resources):
        self.world = world
        self.resources = resources
        
        # Position (in block coordinates)
        self.x = world.width // 2
        self.y = 0
        self.max_depth = 0
        
        # Mining stats (affected by upgrades)
        self.mining_power = Config.BASE_MINING_POWER
        self.mining_speed = Config.BASE_MINING_SPEED
        self.crit_chance = 0.0
        self.crit_multiplier = 2.0
        
        # Passive mining
        self.passive_mining_rate = {}
        self.automation_unlocked = False
        
        # Mining state
        self.current_target = None
        self.last_mine_time = 0
        self.mine_cooldown = 0.5  # Seconds between manual mines
        
        # Visual feedback
        self.last_mined_block = None  # (x, y, timestamp)
        self.particle_effects = []  # List of active particles
        
    def mine(self, upgrades=None):
        """Perform manual mining action"""
        import time as time_module
        current_time = time_module.time()
        if current_time - self.last_mine_time < self.mine_cooldown:
            return False
            
        self.last_mine_time = current_time
        
        # Target block in front of player
        target_x, target_y = self.x, self.y + 1
        block = self.world.get_block(target_x, target_y)
        
        if not block:
            return False
            
        # Apply upgrades
        total_power = self.mining_power
        if upgrades:
            total_power += upgrades.get_total_effect("mining_power")
            
        # Check for critical strike
        is_crit = random.random() < self.crit_chance
        if is_crit:
            total_power *= self.crit_multiplier
            
        # Store block position for visual feedback
        self.last_mined_block = (target_x, target_y, current_time)
        
        # Damage block
        if block.damage(total_power):
            # Block destroyed, collect resources
            self._collect_resources(block, is_crit)
            
            # Move player down
            self.y += 1
            self.max_depth = max(self.max_depth, self.y)
            
            # Reveal surrounding blocks
            self.world.reveal_around(self.x, self.y, 3)
            
        return True
        
    def _collect_resources(self, block, is_crit=False):
        """Collect resources from mined block"""
        for resource_type, amount in block.resources.items():
            # Apply multipliers
            final_amount = amount
            
            if is_crit:
                final_amount *= 1.5  # Bonus for crit
                
            self.resources.add(resource_type, final_amount)
            
    def update(self, dt):
        """Update player state and passive mining"""
        if self.automation_unlocked and self.passive_mining_rate:
            # Passive mining generates resources over time
            for resource_type, rate in self.passive_mining_rate.items():
                if rate > 0:
                    self.resources.add(resource_type, rate * dt)
                    
    def get_passive_mining_rate(self):
        """Get current passive mining rates"""
        return self.passive_mining_rate.copy()
        
    def set_passive_rate(self, resource_type, rate):
        """Set passive mining rate for a resource"""
        self.passive_mining_rate[resource_type] = rate
        
    def add_passive_rate(self, resource_type, rate):
        """Add to passive mining rate"""
        if resource_type not in self.passive_mining_rate:
            self.passive_mining_rate[resource_type] = 0
        self.passive_mining_rate[resource_type] += rate
        self.automation_unlocked = True
        
    def apply_upgrades(self, upgrades):
        """Apply upgrade effects to player stats"""
        # Mining power
        self.mining_power = Config.BASE_MINING_POWER + upgrades.get_total_effect("mining_power")
        
        # Mining speed (affects cooldown)
        speed_bonus = 1.0 + upgrades.get_total_effect("mining_speed")
        self.mine_cooldown = Config.BASE_MINING_SPEED / speed_bonus
        
        # Critical strike
        self.crit_chance = upgrades.get_total_effect("crit_chance")
        self.crit_multiplier = 2.0 + upgrades.get_total_effect("crit_multiplier")
        
        # Passive mining from upgrades
        passive_mining = upgrades.get_total_effect("passive_mining")
        if passive_mining > 0:
            # Distribute across available resources
            self.automation_unlocked = True
            # Simplified: just give passive iron/copper/gold based on depth
            depth_factor = min(self.max_depth / 100, 10)
            self.passive_mining_rate = {
                "iron": passive_mining * 0.5 * depth_factor,
                "copper": passive_mining * 0.3 * depth_factor if self.max_depth >= 50 else 0,
                "gold": passive_mining * 0.15 * depth_factor if self.max_depth >= 150 else 0,
                "crystal": passive_mining * 0.05 * depth_factor if self.max_depth >= 500 else 0
            }
            
    def to_dict(self):
        """Serialize player state"""
        return {
            "x": self.x,
            "y": self.y,
            "max_depth": self.max_depth,
            "mining_power": self.mining_power,
            "mining_speed": self.mining_speed,
            "passive_mining_rate": self.passive_mining_rate,
            "automation_unlocked": self.automation_unlocked
        }
        
    def from_dict(self, data):
        """Load player state"""
        self.x = data.get("x", self.x)
        self.y = data.get("y", self.y)
        self.max_depth = data.get("max_depth", 0)
        self.mining_power = data.get("mining_power", self.mining_power)
        self.mining_speed = data.get("mining_speed", self.mining_speed)
        self.passive_mining_rate = data.get("passive_mining_rate", {})
        self.automation_unlocked = data.get("automation_unlocked", False)
