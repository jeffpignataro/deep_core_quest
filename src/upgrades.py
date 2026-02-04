"""
Upgrade tree system with 50+ nodes
"""

import math

class Upgrade:
    """Single upgrade node"""
    
    def __init__(self, id, name, description, cost, effect_type, effect_value, 
                 prerequisites=None, max_level=None, cost_scaling=1.5):
        self.id = id
        self.name = name
        self.description = description
        self.base_cost = cost  # Dict of {resource: amount}
        self.effect_type = effect_type
        self.effect_value = effect_value
        self.prerequisites = prerequisites or []
        self.max_level = max_level
        self.cost_scaling = cost_scaling
        
        self.level = 0
        self.unlocked = len(self.prerequisites) == 0
        
    def get_cost(self):
        """Get current upgrade cost"""
        if self.max_level and self.level >= self.max_level:
            return None
            
        scaled_cost = {}
        for resource, amount in self.base_cost.items():
            scaled_cost[resource] = math.ceil(amount * math.pow(self.cost_scaling, self.level))
        return scaled_cost
        
    def can_afford(self, resources):
        """Check if upgrade can be afforded"""
        cost = self.get_cost()
        if cost is None:
            return False
        return resources.can_afford_multiple(cost)
        
    def purchase(self, resources):
        """Purchase upgrade"""
        cost = self.get_cost()
        if cost and resources.spend_multiple(cost):
            self.level += 1
            return True
        return False
        
    def get_effect_value(self):
        """Get total effect value at current level"""
        return self.effect_value * self.level
        
    def to_dict(self):
        return {
            "id": self.id,
            "level": self.level,
            "unlocked": self.unlocked
        }
        
    def from_dict(self, data):
        self.level = data.get("level", 0)
        self.unlocked = data.get("unlocked", False)


class UpgradeTree:
    """Manages all upgrades"""
    
    def __init__(self, resources):
        self.resources = resources
        self.upgrades = {}
        self._initialize_upgrades()
        
    def _initialize_upgrades(self):
        """Create all 50+ upgrade nodes"""
        upgrades = [
            # Manual Mining (Tier 1)
            Upgrade("mining_power_1", "Sharper Pickaxe", "Increases mining power by 1", 
                   {"iron": 10}, "mining_power", 1, max_level=10),
            Upgrade("mining_speed_1", "Faster Swings", "Increases mining speed by 10%",
                   {"iron": 15}, "mining_speed", 0.1, max_level=10),
            Upgrade("iron_boost_1", "Iron Detector", "Increases iron drops by 20%",
                   {"iron": 20}, "resource_multiplier", 0.2, max_level=5),
                   
            # Automation (Tier 2)
            Upgrade("auto_drill_1", "Basic Drill", "Unlocks automatic mining (0.5/s)",
                   {"iron": 100, "copper": 50}, "passive_mining", 0.5, 
                   prerequisites=["mining_power_1"]),
            Upgrade("auto_drill_2", "Improved Drill", "Increases auto-mining by 1/s",
                   {"iron": 200, "copper": 100}, "passive_mining", 1.0,
                   prerequisites=["auto_drill_1"], max_level=10),
            Upgrade("conveyor_1", "Conveyor Belt", "Increases resource collection by 50%",
                   {"iron": 150, "copper": 75}, "collection_mult", 0.5,
                   prerequisites=["auto_drill_1"], max_level=5),
                   
            # Copper Mining (Tier 2)
            Upgrade("copper_unlock", "Copper Vein Access", "Unlocks copper mining",
                   {"iron": 200}, "unlock_resource", "copper",
                   prerequisites=["mining_power_1"]),
            Upgrade("copper_boost_1", "Copper Smelting", "Increases copper yield by 30%",
                   {"copper": 50}, "resource_multiplier", 0.3,
                   prerequisites=["copper_unlock"], max_level=5),
                   
            # Depth Access (Tier 2-3)
            Upgrade("depth_1", "Reinforced Gear", "Access depths up to 100m",
                   {"iron": 250, "copper": 100}, "max_depth", 100,
                   prerequisites=["mining_power_1"]),
            Upgrade("depth_2", "Advanced Gear", "Access depths up to 250m",
                   {"iron": 500, "copper": 300, "gold": 50}, "max_depth", 250,
                   prerequisites=["depth_1"]),
                   
            # Gold Mining (Tier 3)
            Upgrade("gold_unlock", "Gold Vein Access", "Unlocks gold mining",
                   {"iron": 500, "copper": 250}, "unlock_resource", "gold",
                   prerequisites=["depth_1"]),
            Upgrade("gold_boost_1", "Gold Refining", "Increases gold yield by 40%",
                   {"gold": 100}, "resource_multiplier", 0.4,
                   prerequisites=["gold_unlock"], max_level=5),
                   
            # Advanced Automation (Tier 3)
            Upgrade("robotic_arm_1", "Robotic Mining Arm", "Adds 5/s passive mining",
                   {"iron": 1000, "copper": 500, "gold": 200}, "passive_mining", 5.0,
                   prerequisites=["auto_drill_2", "gold_unlock"]),
            Upgrade("robotic_arm_2", "Enhanced Robotic Arm", "Adds 10/s passive mining",
                   {"iron": 2000, "copper": 1000, "gold": 500}, "passive_mining", 10.0,
                   prerequisites=["robotic_arm_1"], max_level=10),
                   
            # Efficiency (Tier 3)
            Upgrade("efficiency_1", "Optimized Systems", "Increases all production by 25%",
                   {"gold": 250}, "global_multiplier", 0.25,
                   prerequisites=["conveyor_1"], max_level=10),
            Upgrade("efficiency_2", "AI Optimization", "Increases all production by 50%",
                   {"gold": 500, "crystal": 100}, "global_multiplier", 0.50,
                   prerequisites=["efficiency_1"], max_level=5),
                   
            # Deep Mining (Tier 4)
            Upgrade("depth_3", "Volcanic Suit", "Access depths up to 500m",
                   {"iron": 2000, "copper": 1000, "gold": 500}, "max_depth", 500,
                   prerequisites=["depth_2"]),
            Upgrade("depth_4", "Crystal Shielding", "Access depths up to 750m",
                   {"gold": 1000, "crystal": 500}, "max_depth", 750,
                   prerequisites=["depth_3"]),
                   
            # Crystal Mining (Tier 4)
            Upgrade("crystal_unlock", "Crystal Cavern Access", "Unlocks crystal mining",
                   {"gold": 1000, "iron": 2000}, "unlock_resource", "crystal",
                   prerequisites=["depth_3"]),
            Upgrade("crystal_boost_1", "Crystal Resonance", "Increases crystal yield by 50%",
                   {"crystal": 200}, "resource_multiplier", 0.5,
                   prerequisites=["crystal_unlock"], max_level=5),
                   
            # Mega Automation (Tier 4)
            Upgrade("mega_drill_1", "Mega Drill Array", "Adds 50/s passive mining",
                   {"gold": 5000, "crystal": 1000}, "passive_mining", 50.0,
                   prerequisites=["robotic_arm_2", "crystal_unlock"]),
            Upgrade("mega_drill_2", "Hyper Drill Array", "Adds 100/s passive mining",
                   {"gold": 10000, "crystal": 2500}, "passive_mining", 100.0,
                   prerequisites=["mega_drill_1"], max_level=10),
                   
            # Special Abilities (Tier 4)
            Upgrade("earthquake_1", "Seismic Blast", "Reveals hidden veins (active ability)",
                   {"gold": 1500, "crystal": 500}, "ability", "earthquake",
                   prerequisites=["depth_3"]),
            Upgrade("xray_vision", "Mineral Scanner", "See resource distribution",
                   {"gold": 2000, "crystal": 750}, "ability", "xray",
                   prerequisites=["crystal_unlock"]),
                   
            # Ancient Depths (Tier 5)
            Upgrade("depth_5", "Ancient Relic Armor", "Access depths up to 1000m",
                   {"gold": 5000, "crystal": 2000}, "max_depth", 1000,
                   prerequisites=["depth_4"]),
            Upgrade("artifact_unlock", "Relic Hunter", "Unlocks artifact collection",
                   {"crystal": 3000}, "unlock_resource", "artifact",
                   prerequisites=["depth_5"]),
                   
            # Prestige Prep (Tier 5)
            Upgrade("prestige_ready", "Core Breach Technology", "Enables prestige at depth 1000",
                   {"gold": 10000, "crystal": 5000, "artifact": 100}, "unlock", "prestige",
                   prerequisites=["depth_5", "artifact_unlock"]),
                   
            # Multiplier Upgrades (Cross-tier)
            Upgrade("multi_iron_1", "Iron Abundance", "+100% iron from all sources",
                   {"iron": 500}, "resource_multiplier", 1.0, max_level=5),
            Upgrade("multi_copper_1", "Copper Abundance", "+100% copper from all sources",
                   {"copper": 500}, "resource_multiplier", 1.0,
                   prerequisites=["copper_unlock"], max_level=5),
            Upgrade("multi_gold_1", "Gold Abundance", "+100% gold from all sources",
                   {"gold": 1000}, "resource_multiplier", 1.0,
                   prerequisites=["gold_unlock"], max_level=5),
            Upgrade("multi_crystal_1", "Crystal Abundance", "+100% crystal from all sources",
                   {"crystal": 1000}, "resource_multiplier", 1.0,
                   prerequisites=["crystal_unlock"], max_level=5),
                   
            # Speed Upgrades
            Upgrade("speed_boost_1", "Swift Mining I", "+20% mining speed",
                   {"iron": 100}, "mining_speed", 0.2, max_level=5),
            Upgrade("speed_boost_2", "Swift Mining II", "+40% mining speed",
                   {"copper": 200}, "mining_speed", 0.4,
                   prerequisites=["speed_boost_1"], max_level=5),
            Upgrade("speed_boost_3", "Swift Mining III", "+80% mining speed",
                   {"gold": 500}, "mining_speed", 0.8,
                   prerequisites=["speed_boost_2"], max_level=5),
                   
            # Power Upgrades
            Upgrade("power_boost_1", "Mighty Swing I", "+2 mining power",
                   {"iron": 150}, "mining_power", 2, max_level=5),
            Upgrade("power_boost_2", "Mighty Swing II", "+5 mining power",
                   {"copper": 300}, "mining_power", 5,
                   prerequisites=["power_boost_1"], max_level=5),
            Upgrade("power_boost_3", "Mighty Swing III", "+10 mining power",
                   {"gold": 750}, "mining_power", 10,
                   prerequisites=["power_boost_2"], max_level=5),
                   
            # Advanced Power
            Upgrade("power_mega_1", "Titan Strength", "+50 mining power",
                   {"gold": 2000, "crystal": 500}, "mining_power", 50,
                   prerequisites=["power_boost_3"], max_level=10),
                   
            # Collection Upgrades
            Upgrade("collection_2", "Magnetic Collectors", "+100% collection efficiency",
                   {"gold": 1000}, "collection_mult", 1.0,
                   prerequisites=["conveyor_1"], max_level=5),
            Upgrade("collection_3", "Quantum Collectors", "+200% collection efficiency",
                   {"crystal": 1500}, "collection_mult", 2.0,
                   prerequisites=["collection_2"], max_level=5),
                   
            # Combo Upgrades
            Upgrade("combo_speed_power", "Precision Impact", "+25% speed, +25% power",
                   {"gold": 1500}, "combo", {"mining_speed": 0.25, "mining_power": 0.25},
                   prerequisites=["speed_boost_2", "power_boost_2"], max_level=3),
                   
            # Passive Income Boosts
            Upgrade("passive_boost_1", "Drone Efficiency I", "+50% passive mining rate",
                   {"gold": 800}, "passive_multiplier", 0.5,
                   prerequisites=["auto_drill_2"], max_level=10),
            Upgrade("passive_boost_2", "Drone Efficiency II", "+100% passive mining rate",
                   {"crystal": 1200}, "passive_multiplier", 1.0,
                   prerequisites=["passive_boost_1"], max_level=10),
                   
            # Offline Bonuses
            Upgrade("offline_bonus_1", "Autonomous Mode I", "+50% offline generation",
                   {"gold": 1000}, "offline_mult", 0.5, max_level=5),
            Upgrade("offline_bonus_2", "Autonomous Mode II", "+100% offline generation",
                   {"crystal": 2000}, "offline_mult", 1.0,
                   prerequisites=["offline_bonus_1"], max_level=5),
                   
            # Critical Strike
            Upgrade("crit_chance_1", "Critical Mining", "5% chance for 2x resources",
                   {"copper": 500}, "crit_chance", 0.05,
                   prerequisites=["mining_power_1"], max_level=10),
            Upgrade("crit_damage_1", "Critical Power", "Critical strikes give 3x instead of 2x",
                   {"gold": 1000}, "crit_multiplier", 1.0,
                   prerequisites=["crit_chance_1"], max_level=5),
                   
            # Exploration
            Upgrade("exploration_1", "Cave Mapper", "Reveals nearby resources",
                   {"copper": 300}, "ability", "map", prerequisites=["depth_1"]),
            Upgrade("exploration_2", "Deep Scanner", "Reveals all resources in current layer",
                   {"gold": 1500}, "ability", "deep_scan",
                   prerequisites=["exploration_1"]),
                   
            # Lucky Drops
            Upgrade("luck_1", "Fortune I", "+10% chance for bonus resources",
                   {"gold": 500}, "luck", 0.1, max_level=10),
            Upgrade("luck_2", "Fortune II", "+20% chance for bonus resources",
                   {"crystal": 1000}, "luck", 0.2,
                   prerequisites=["luck_1"], max_level=10),
                   
            # Boss Upgrades
            Upgrade("boss_damage", "Boss Slayer", "+50% damage to boss rocks",
                   {"gold": 2000}, "boss_damage", 0.5, max_level=5),
            Upgrade("boss_rewards", "Relic Hunter", "+100% rewards from bosses",
                   {"crystal": 2500}, "boss_rewards", 1.0,
                   prerequisites=["boss_damage"], max_level=5),
        ]
        
        for upgrade in upgrades:
            self.upgrades[upgrade.id] = upgrade
            
    def get_upgrade(self, upgrade_id):
        """Get upgrade by ID"""
        return self.upgrades.get(upgrade_id)
        
    def purchase_upgrade(self, upgrade_id):
        """Purchase an upgrade"""
        upgrade = self.get_upgrade(upgrade_id)
        if upgrade and upgrade.purchase(self.resources):
            self._check_unlock_prerequisites()
            return True
        return False
        
    def _check_unlock_prerequisites(self):
        """Check and unlock upgrades whose prerequisites are met"""
        for upgrade in self.upgrades.values():
            if not upgrade.unlocked:
                prereqs_met = all(
                    self.upgrades[prereq_id].level > 0
                    for prereq_id in upgrade.prerequisites
                    if prereq_id in self.upgrades
                )
                if prereqs_met:
                    upgrade.unlocked = True
                    
    def get_total_effect(self, effect_type):
        """Get total effect value of a specific type"""
        total = 0
        for upgrade in self.upgrades.values():
            if upgrade.effect_type == effect_type and upgrade.level > 0:
                total += upgrade.get_effect_value()
        return total
        
    def has_ability(self, ability_name):
        """Check if player has unlocked an ability"""
        for upgrade in self.upgrades.values():
            if upgrade.effect_type == "ability" and upgrade.effect_value == ability_name:
                return upgrade.level > 0
        return False
        
    def get_unlocked_upgrades(self):
        """Get list of unlocked upgrades"""
        return [u for u in self.upgrades.values() if u.unlocked]
        
    def update(self, dt):
        """Update upgrade system"""
        pass
        
    def to_dict(self):
        """Serialize to dict"""
        return {
            upgrade_id: upgrade.to_dict()
            for upgrade_id, upgrade in self.upgrades.items()
        }
        
    def from_dict(self, data):
        """Load from dict"""
        for upgrade_id, upgrade_data in data.items():
            if upgrade_id in self.upgrades:
                self.upgrades[upgrade_id].from_dict(upgrade_data)
        self._check_unlock_prerequisites()
