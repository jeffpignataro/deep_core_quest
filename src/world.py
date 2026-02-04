"""
Procedural world generation with layers and biomes
"""

import pygame
import random
import noise
from .config import Config

class Block:
    """Individual block in the world"""
    
    def __init__(self, x, y, block_type, hardness, resources):
        self.x = x
        self.y = y
        self.type = block_type
        self.hardness = hardness
        self.resources = resources  # Dict of resource: amount
        self.health = hardness
        self.visible = False
        
    def damage(self, amount):
        """Apply damage to block"""
        self.health -= amount
        return self.health <= 0
        
    def reset_health(self):
        """Reset block health"""
        self.health = self.hardness


class Layer:
    """World layer/biome"""
    
    def __init__(self, name, depth_start, depth_end, hardness_mult, resources):
        self.name = name
        self.depth_start = depth_start
        self.depth_end = depth_end
        self.hardness_mult = hardness_mult
        self.resources = resources  # List of (resource_type, weight)
        self.color = Config.LAYER_COLORS.get(name, (100, 100, 100))
        
    def contains_depth(self, depth):
        """Check if this layer contains the given depth"""
        return self.depth_start <= depth < self.depth_end


class World:
    """Procedurally generated world"""
    
    def __init__(self, width=5, height=2000):
        self.width = width
        self.height = height
        self.blocks = {}
        
        # Define layers
        self.layers = [
            Layer("surface", 0, 50, 1.0, [("iron", 10), ("copper", 2)]),
            Layer("cave", 50, 150, 1.5, [("iron", 8), ("copper", 5), ("gold", 1)]),
            Layer("deep_cave", 150, 300, 2.0, [("copper", 10), ("gold", 3), ("iron", 5)]),
            Layer("volcanic", 300, 500, 3.0, [("gold", 10), ("crystal", 2), ("copper", 5)]),
            Layer("crystal", 500, 750, 4.0, [("crystal", 10), ("gold", 5), ("artifact", 1)]),
            Layer("ancient", 750, 1000, 5.0, [("artifact", 5), ("crystal", 8), ("gold", 5)]),
            Layer("core", 1000, 2000, 10.0, [("artifact", 10), ("crystal", 10)])
        ]
        
        self.current_layer = self.layers[0]
        self.seed = random.randint(0, 1000000)
        
        # Generate initial visible area
        self._generate_area(0, 0, width, 100)
        
    def get_layer_at_depth(self, depth):
        """Get layer at specific depth"""
        for layer in self.layers:
            if layer.contains_depth(depth):
                return layer
        return self.layers[-1]
        
    def _generate_area(self, x_start, y_start, x_end, y_end):
        """Generate blocks in an area"""
        for y in range(y_start, min(y_end, self.height)):
            layer = self.get_layer_at_depth(y)
            
            for x in range(x_start, x_end):
                if (x, y) in self.blocks:
                    continue
                    
                # Use Perlin noise for varied hardness
                noise_val = noise.pnoise2(
                    x * 0.1 + self.seed,
                    y * 0.1,
                    octaves=3,
                    persistence=0.5,
                    lacunarity=2.0
                )
                
                # Base hardness with noise variation
                hardness = layer.hardness_mult * (10 + noise_val * 5)
                
                # Determine resources
                resources = self._generate_resources(layer, x, y)
                
                block_type = "rock"
                if resources:
                    # Visual indicator of valuable blocks
                    block_type = list(resources.keys())[0]
                    
                block = Block(x, y, block_type, hardness, resources)
                self.blocks[(x, y)] = block
                
    def _generate_resources(self, layer, x, y):
        """Generate resources for a block"""
        resources = {}
        
        # Dirt percentage: 90% at surface (depth 0), 40% at depth 500+
        depth = y
        if depth < 500:
            dirt_chance = 0.9 - (depth / 500) * 0.5  # Linear scale from 90% to 40%
        else:
            dirt_chance = 0.4
            
        # Check if this block is dirt (no resources)
        dirt_noise = noise.pnoise2(
            x * 1.2 + self.seed + 9999,
            y * 0.4,
            octaves=2
        )
        dirt_threshold = (dirt_noise + 1.0) / 2.0  # Normalize to 0-1
        
        if dirt_threshold < dirt_chance:
            # Dirt block - no resources
            return {}
        
        # Resource block - vary by position
        if layer.resources:
            # Determine which resource type for this specific block
            # Use high-frequency noise for more variation in narrow width
            primary_noise = noise.pnoise2(
                x * 0.8 + self.seed,  # Much higher frequency for 5-block width
                y * 0.3,
                octaves=3
            )
            
            # Pick resource type based on noise and layer distribution
            total_weight = sum(w for _, w in layer.resources)
            threshold = (primary_noise + 1.0) / 2.0  # Normalize to 0-1
            
            accumulated = 0
            selected_resource = layer.resources[0][0]
            selected_weight = layer.resources[0][1]
            
            for resource_type, weight in layer.resources:
                accumulated += weight / total_weight
                if threshold <= accumulated:
                    selected_resource = resource_type
                    selected_weight = weight
                    break
            
            # Amount variation using different noise
            amount_noise = noise.pnoise2(
                x * 0.5 + self.seed + hash(selected_resource) % 1000,
                y * 0.2,
                octaves=2
            )
            
            amount = selected_weight * (1.0 + max(0, amount_noise))
            resources[selected_resource] = amount
                
        return resources
        
    def get_block(self, x, y):
        """Get block at position"""
        if (x, y) not in self.blocks:
            self._generate_area(x, y, x + 1, y + 1)
        return self.blocks.get((x, y))
        
    def remove_block(self, x, y):
        """Remove/mine a block"""
        block = self.get_block(x, y)
        if block:
            resources = block.resources.copy()
            # Regenerate block after mining
            block.reset_health()
            return resources
        return {}
        
    def reveal_around(self, x, y, radius):
        """Reveal blocks in radius"""
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                block = self.get_block(x + dx, y + dy)
                if block:
                    block.visible = True
                    
    def render(self, screen, player):
        """Render visible world"""
        import time
        block_size = 128  # Double size for 4K clarity
        viewport_x = player.x - Config.SCREEN_WIDTH // (2 * block_size)
        viewport_y = player.y - Config.SCREEN_HEIGHT // (2 * block_size)
        
        for y in range(int(viewport_y), int(viewport_y + Config.SCREEN_HEIGHT // block_size + 2)):
            for x in range(int(viewport_x), int(viewport_x + Config.SCREEN_WIDTH // block_size + 2)):
                block = self.get_block(x, y)
                if not block:
                    continue
                    
                # Screen position
                screen_x = (x - viewport_x) * block_size
                screen_y = (y - viewport_y) * block_size
                
                if screen_x < 0 or screen_x >= Config.SCREEN_WIDTH // 2:
                    continue
                if screen_y < 0 or screen_y >= Config.SCREEN_HEIGHT:
                    continue
                    
                # Determine base color from layer
                layer = self.get_layer_at_depth(y)
                color = layer.color
                
                # Highlight resource blocks
                if block.resources:
                    resource_type = list(block.resources.keys())[0]
                    resource_color = Config.RESOURCE_COLORS.get(resource_type, color)
                    color = tuple(min(255, c + 30) for c in resource_color)
                    
                # Darken if damaged (not at full health)
                if block.health < block.hardness:
                    # Show damage
                    damage_ratio = block.health / block.hardness
                    color = tuple(int(c * damage_ratio) for c in color)
                
                # Click feedback - white flash on recently clicked block
                if player.last_clicked_block:
                    clicked_x, clicked_y, click_time = player.last_clicked_block
                    if x == clicked_x and y == clicked_y:
                        elapsed = time.time() - click_time
                        if elapsed < 0.2:  # Short 200ms flash
                            flash_intensity = 1.0 - (elapsed / 0.2)
                            color = tuple(
                                int(c + (255 - c) * flash_intensity * 0.5)  # 50% flash intensity
                                for c in color
                            )
                    
                pygame.draw.rect(screen, color, (screen_x, screen_y, block_size, block_size))
                pygame.draw.rect(screen, (0, 0, 0), (screen_x, screen_y, block_size, block_size), 1)
                
    def update(self, dt):
        """Update world"""
        pass
        
    def to_dict(self):
        """Serialize world state"""
        return {
            "seed": self.seed,
            "width": self.width,
            "height": self.height
        }
        
    def from_dict(self, data):
        """Load world state"""
        self.seed = data.get("seed", self.seed)
        self.width = data.get("width", self.width)
        self.height = data.get("height", self.height)
        # Regenerate world with saved seed
        self.blocks = {}
        self._generate_area(0, 0, self.width, 100)
