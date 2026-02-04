"""
User interface rendering and interaction
"""

import pygame
# Import font after pygame to avoid circular import issues
from pygame import font as pgfont
from .config import Config

class Button:
    """Clickable button"""
    
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
        
    def handle_click(self, pos):
        """Check if button was clicked"""
        if self.rect.collidepoint(pos):
            self.callback()
            return True
        return False
        
    def update_hover(self, pos):
        """Update hover state"""
        self.hovered = self.rect.collidepoint(pos)
        
    def render(self, screen, font):
        """Render button"""
        color = Config.HIGHLIGHT_COLOR if self.hovered else Config.UI_BORDER_COLOR
        pygame.draw.rect(screen, Config.UI_BG_COLOR, self.rect)
        pygame.draw.rect(screen, color, self.rect, 2)
        
        text_surf = font.render(self.text, True, Config.TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


class UI:
    """Main UI manager"""
    
    def __init__(self, resources, upgrades, player, world):
        self.resources = resources
        self.upgrades = upgrades
        self.player = player
        self.world = world
        
        # Fonts - ensure font module is initialized
        if not pgfont.get_init():
            pgfont.init()
        self.font = pgfont.Font(None, 72)
        self.title_font = pgfont.Font(None, 96)
        self.small_font = pgfont.Font(None, 54)
        
        # UI state
        self.selected_upgrade = None
        self.upgrade_scroll = 0
        self.notification = None
        self.notification_time = 0
        
        # Buttons
        self.buttons = []
        self._create_buttons()
        
    def _create_buttons(self):
        """Create UI buttons"""
        # Prestige button (shown when available)
        self.prestige_button = Button(
            Config.SCREEN_WIDTH - 220, 20, 200, 40,
            "PRESTIGE",
            self._handle_prestige
        )
        
    def handle_click(self, pos, button):
        """Handle mouse click"""
        if button == 1:  # Left click
            # Check upgrade list
            self._handle_upgrade_click(pos)
            
            # Check buttons
            self.prestige_button.handle_click(pos)
            
    def _handle_upgrade_click(self, pos):
        """Handle click on upgrade list"""
        upgrade_panel_x = Config.SCREEN_WIDTH // 2 + 20
        upgrade_panel_y = 60
        upgrade_height = 80
        
        mouse_x, mouse_y = pos
        
        if mouse_x < upgrade_panel_x or mouse_x > Config.SCREEN_WIDTH - 20:
            return
        if mouse_y < upgrade_panel_y:
            return
            
        # Determine which upgrade was clicked
        index = (mouse_y - upgrade_panel_y + self.upgrade_scroll) // upgrade_height
        unlocked_upgrades = self.upgrades.get_unlocked_upgrades()
        
        if 0 <= index < len(unlocked_upgrades):
            upgrade = unlocked_upgrades[index]
            if upgrade.can_afford(self.resources):
                if self.upgrades.purchase_upgrade(upgrade.id):
                    self.player.apply_upgrades(self.upgrades)
                    self.show_notification(f"Purchased: {upgrade.name}")
                    
    def _handle_prestige(self):
        """Handle prestige button click"""
        if self.player.max_depth >= Config.PRESTIGE_DEPTH:
            if self.upgrades.has_ability("prestige"):
                self.resources.prestige()
                self.player.y = 0
                self.player.max_depth = 0
                # Reset upgrades
                for upgrade in self.upgrades.upgrades.values():
                    upgrade.level = 0
                    upgrade.unlocked = len(upgrade.prerequisites) == 0
                self.show_notification(f"PRESTIGE! Level {self.resources.prestige_level}")
                
    def update(self, dt):
        """Update UI state"""
        # Update hover states
        mouse_pos = pygame.mouse.get_pos()
        self.prestige_button.update_hover(mouse_pos)
        
        # Update notifications
        if self.notification:
            self.notification_time -= dt
            if self.notification_time <= 0:
                self.notification = None
                
    def render(self, screen):
        """Render UI"""
        # Resource panel
        self._render_resource_panel(screen)
        
        # Upgrade panel
        self._render_upgrade_panel(screen)
        
        # Stats panel
        self._render_stats_panel(screen)
        
        # Prestige button (if available)
        if self.player.max_depth >= Config.PRESTIGE_DEPTH and self.upgrades.has_ability("prestige"):
            self.prestige_button.render(screen, self.font)
            
        # Notifications
        if self.notification:
            self._render_notification(screen)
            
    def _render_resource_panel(self, screen):
        """Render resource display"""
        panel_x = Config.SCREEN_WIDTH // 2 + 20
        panel_y = 20
        panel_width = Config.SCREEN_WIDTH // 2 - 40
        panel_height = 150
        
        pygame.draw.rect(screen, Config.UI_BG_COLOR, (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, Config.UI_BORDER_COLOR, (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Title
        title = self.title_font.render("Resources", True, Config.HIGHLIGHT_COLOR)
        screen.blit(title, (panel_x + 10, panel_y + 10))
        
        # Resources
        y_offset = panel_y + 50
        for i, (resource_type, amount) in enumerate(self.resources.resources.items()):
            color = Config.RESOURCE_COLORS.get(resource_type, Config.TEXT_COLOR)
            
            # Resource name and amount
            text = f"{resource_type.capitalize()}: {amount:.0f}"
            resource_surf = self.font.render(text, True, color)
            screen.blit(resource_surf, (panel_x + 20, y_offset))
            
            # Passive rate if > 0
            rate = self.resources.passive_rates.get(resource_type, 0)
            if rate > 0:
                rate_text = f"(+{rate:.1f}/s)"
                rate_surf = self.small_font.render(rate_text, True, color)
                screen.blit(rate_surf, (panel_x + 220, y_offset + 5))
                
            y_offset += 25
            if i == 2:  # Move to second column
                y_offset = panel_y + 50
                panel_x += 250
                
    def _render_upgrade_panel(self, screen):
        """Render upgrade list"""
        panel_x = Config.SCREEN_WIDTH // 2 + 20
        panel_y = 180
        panel_width = Config.SCREEN_WIDTH // 2 - 40
        panel_height = Config.SCREEN_HEIGHT - 200
        
        pygame.draw.rect(screen, Config.UI_BG_COLOR, (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, Config.UI_BORDER_COLOR, (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Title
        title = self.title_font.render("Upgrades", True, Config.HIGHLIGHT_COLOR)
        screen.blit(title, (panel_x + 10, panel_y + 10))
        
        # Upgrade list
        y_offset = panel_y + 50
        unlocked_upgrades = self.upgrades.get_unlocked_upgrades()
        
        for upgrade in unlocked_upgrades:
            if y_offset > panel_y + panel_height - 80:
                break
                
            # Upgrade background
            upgrade_rect = pygame.Rect(panel_x + 10, y_offset, panel_width - 20, 70)
            can_afford = upgrade.can_afford(self.resources)
            bg_color = (60, 80, 60) if can_afford else Config.UI_BG_COLOR
            pygame.draw.rect(screen, bg_color, upgrade_rect)
            pygame.draw.rect(screen, Config.UI_BORDER_COLOR, upgrade_rect, 1)
            
            # Upgrade name and level
            name_text = f"{upgrade.name} (Lv {upgrade.level})"
            if upgrade.max_level:
                name_text += f" / {upgrade.max_level}"
            name_surf = self.font.render(name_text, True, Config.TEXT_COLOR)
            screen.blit(name_surf, (panel_x + 20, y_offset + 5))
            
            # Description
            desc_surf = self.small_font.render(upgrade.description, True, Config.TEXT_COLOR)
            screen.blit(desc_surf, (panel_x + 20, y_offset + 28))
            
            # Cost
            cost = upgrade.get_cost()
            if cost:
                cost_text = ", ".join([f"{amt:.0f} {res}" for res, amt in cost.items()])
                cost_surf = self.small_font.render(f"Cost: {cost_text}", True, 
                                                  Config.HIGHLIGHT_COLOR if can_afford else (150, 150, 150))
                screen.blit(cost_surf, (panel_x + 20, y_offset + 48))
            else:
                max_surf = self.small_font.render("MAX LEVEL", True, Config.HIGHLIGHT_COLOR)
                screen.blit(max_surf, (panel_x + 20, y_offset + 48))
                
            y_offset += 80
            
    def _render_stats_panel(self, screen):
        """Render player stats"""
        panel_x = 20
        panel_y = 20
        panel_width = Config.SCREEN_WIDTH // 2 - 40
        panel_height = 120
        
        pygame.draw.rect(screen, Config.UI_BG_COLOR, (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, Config.UI_BORDER_COLOR, (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Title
        title = self.title_font.render("Stats", True, Config.HIGHLIGHT_COLOR)
        screen.blit(title, (panel_x + 10, panel_y + 10))
        
        # Stats
        stats = [
            f"Depth: {self.player.y}m (Max: {self.player.max_depth}m)",
            f"Mining Power: {self.player.mining_power:.1f}",
            f"Mining Speed: {1/self.player.mine_cooldown:.1f} hits/s",
            f"Prestige Level: {self.resources.prestige_level} ({self.resources.prestige_multiplier:.1f}x)"
        ]
        
        y_offset = panel_y + 45
        for stat in stats:
            stat_surf = self.small_font.render(stat, True, Config.TEXT_COLOR)
            screen.blit(stat_surf, (panel_x + 20, y_offset))
            y_offset += 20
            
    def _render_notification(self, screen):
        """Render notification popup"""
        if not self.notification:
            return
            
        text_surf = self.title_font.render(self.notification, True, Config.HIGHLIGHT_COLOR)
        text_rect = text_surf.get_rect(center=(Config.SCREEN_WIDTH // 2, 50))
        
        # Background
        bg_rect = text_rect.inflate(40, 20)
        pygame.draw.rect(screen, Config.UI_BG_COLOR, bg_rect)
        pygame.draw.rect(screen, Config.HIGHLIGHT_COLOR, bg_rect, 2)
        
        screen.blit(text_surf, text_rect)
        
    def show_notification(self, text, duration=2.0):
        """Show a notification"""
        self.notification = text
        self.notification_time = duration
        
    def show_offline_notification(self, offline_seconds, resources):
        """Show offline progress notification"""
        hours = offline_seconds / 3600
        resource_text = ", ".join([f"{amt:.0f} {res}" for res, amt in resources.items() if amt > 0])
        text = f"Offline for {hours:.1f}h - Earned: {resource_text}"
        self.show_notification(text, duration=5.0)
