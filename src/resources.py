"""
Resource management system
"""

import math

class ResourceManager:
    """Manages all game resources"""
    
    def __init__(self):
        self.resources = {
            "iron": 0,
            "copper": 0,
            "gold": 0,
            "crystal": 0,
            "artifact": 0
        }
        
        # Resource generation rates (per second)
        self.passive_rates = {
            "iron": 0,
            "copper": 0,
            "gold": 0,
            "crystal": 0,
            "artifact": 0
        }
        
        # Prestige multipliers
        self.prestige_level = 0
        self.prestige_multiplier = 1.0
        
    def add(self, resource_type, amount):
        """Add resources"""
        if resource_type in self.resources:
            self.resources[resource_type] += amount * self.prestige_multiplier
            return True
        return False
        
    def spend(self, resource_type, amount):
        """Spend resources if available"""
        if self.can_afford(resource_type, amount):
            self.resources[resource_type] -= amount
            return True
        return False
        
    def can_afford(self, resource_type, amount):
        """Check if player can afford cost"""
        if resource_type in self.resources:
            return self.resources[resource_type] >= amount
        return False
        
    def can_afford_multiple(self, costs):
        """Check if player can afford multiple resource costs"""
        for resource_type, amount in costs.items():
            if not self.can_afford(resource_type, amount):
                return False
        return True
        
    def spend_multiple(self, costs):
        """Spend multiple resource types"""
        if not self.can_afford_multiple(costs):
            return False
            
        for resource_type, amount in costs.items():
            self.spend(resource_type, amount)
        return True
        
    def get(self, resource_type):
        """Get amount of resource"""
        return self.resources.get(resource_type, 0)
        
    def set_passive_rate(self, resource_type, rate):
        """Set passive generation rate"""
        if resource_type in self.passive_rates:
            self.passive_rates[resource_type] = rate
            
    def add_passive_rate(self, resource_type, rate):
        """Add to passive generation rate"""
        if resource_type in self.passive_rates:
            self.passive_rates[resource_type] += rate
            
    def update(self, dt):
        """Update passive resource generation"""
        for resource_type, rate in self.passive_rates.items():
            if rate > 0:
                self.add(resource_type, rate * dt)
                
    def prestige(self):
        """Perform prestige reset"""
        self.prestige_level += 1
        self.prestige_multiplier = math.pow(1.5, self.prestige_level)
        
        # Reset resources but keep artifacts
        artifacts = self.resources["artifact"]
        self.resources = {
            "iron": 0,
            "copper": 0,
            "gold": 0,
            "crystal": 0,
            "artifact": artifacts
        }
        
        self.passive_rates = {
            "iron": 0,
            "copper": 0,
            "gold": 0,
            "crystal": 0,
            "artifact": 0
        }
        
    def to_dict(self):
        """Serialize to dict"""
        return {
            "resources": self.resources.copy(),
            "passive_rates": self.passive_rates.copy(),
            "prestige_level": self.prestige_level,
            "prestige_multiplier": self.prestige_multiplier
        }
        
    def from_dict(self, data):
        """Load from dict"""
        self.resources = data.get("resources", self.resources)
        self.passive_rates = data.get("passive_rates", self.passive_rates)
        self.prestige_level = data.get("prestige_level", 0)
        self.prestige_multiplier = data.get("prestige_multiplier", 1.0)
