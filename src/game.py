"""
Main game class and game loop
"""

import pygame
import time
import json
import os
from pathlib import Path

from .resources import ResourceManager
from .upgrades import UpgradeTree
from .world import World
from .player import Player
from .ui import UI
from .config import Config

class Game:
    """Main game class handling game loop and state"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("Deep Core Quest")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.resources = ResourceManager()
        self.upgrades = UpgradeTree(self.resources)
        self.world = World()
        self.player = Player(self.world, self.resources)
        self.ui = UI(self.resources, self.upgrades, self.player, self.world)
        
        # Time tracking
        self.last_tick = time.time()
        self.offline_time = 0
        
        # Try to load save
        self.load_game()
        
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(Config.FPS) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.render()
            
        self.save_game()
            
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.save_game()
                    print("Game saved!")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Let UI handle the click first
                ui_handled = self.ui.handle_click(event.pos, event.button)
                
                # Manual mining click - only if UI didn't handle it
                if not ui_handled and event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    # Only mine if clicking on the world (left half of screen)
                    if mouse_pos[0] < Config.SCREEN_WIDTH // 2:
                        self.player.mine(self.upgrades)
                        
    def update(self, dt):
        """Update game state"""
        current_time = time.time()
        
        # Passive resource generation
        self.player.update(dt)
        self.resources.update(dt)
        self.upgrades.update(dt)
        self.world.update(dt)
        self.ui.update(dt)
        
        self.last_tick = current_time
        
    def render(self):
        """Render game"""
        self.screen.fill(Config.BG_COLOR)
        
        # Render world
        self.world.render(self.screen, self.player)
        
        # Render UI
        self.ui.render(self.screen)
        
        pygame.display.flip()
        
    def save_game(self):
        """Save game state to file"""
        save_dir = Path.home() / ".deep_core_quest"
        save_dir.mkdir(exist_ok=True)
        save_file = save_dir / "save.json"
        
        save_data = {
            "last_save": time.time(),
            "resources": self.resources.to_dict(),
            "upgrades": self.upgrades.to_dict(),
            "player": self.player.to_dict(),
            "world": self.world.to_dict()
        }
        
        with open(save_file, 'w') as f:
            json.dump(save_data, f, indent=2)
            
    def load_game(self):
        """Load game state from file"""
        save_file = Path.home() / ".deep_core_quest" / "save.json"
        
        if not save_file.exists():
            return
            
        try:
            with open(save_file, 'r') as f:
                save_data = json.load(f)
                
            # Calculate offline time
            last_save = save_data.get("last_save", time.time())
            self.offline_time = time.time() - last_save
            
            # Load game state
            self.resources.from_dict(save_data.get("resources", {}))
            self.upgrades.from_dict(save_data.get("upgrades", {}))
            self.player.from_dict(save_data.get("player", {}))
            self.world.from_dict(save_data.get("world", {}))
            
            # Apply offline progression
            if self.offline_time > 0:
                self.apply_offline_progress()
                
            print(f"Game loaded! Offline for {self.offline_time/60:.1f} minutes")
            
        except Exception as e:
            print(f"Error loading save: {e}")
            
    def apply_offline_progress(self):
        """Apply offline resource generation"""
        # Cap offline time to 8 hours
        offline_seconds = min(self.offline_time, 8 * 3600)
        
        # Generate resources based on passive income
        passive_rate = self.player.get_passive_mining_rate()
        offline_resources = {}
        
        for resource_type in ["iron", "copper", "gold", "crystal"]:
            amount = passive_rate.get(resource_type, 0) * offline_seconds
            if amount > 0:
                offline_resources[resource_type] = amount
                self.resources.add(resource_type, amount)
                
        self.ui.show_offline_notification(offline_seconds, offline_resources)
