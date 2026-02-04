"""
Game configuration and constants
"""

class Config:
    """Global game configuration"""
    
    # Display
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = 60
    
    # Colors
    BG_COLOR = (20, 15, 25)
    UI_BG_COLOR = (40, 35, 45)
    UI_BORDER_COLOR = (80, 70, 90)
    TEXT_COLOR = (220, 220, 220)
    HIGHLIGHT_COLOR = (255, 200, 50)
    
    # Layer colors (procedurally vary these)
    LAYER_COLORS = {
        "surface": (139, 90, 43),
        "cave": (90, 70, 50),
        "deep_cave": (70, 55, 40),
        "volcanic": (140, 40, 30),
        "crystal": (100, 50, 120),
        "ancient": (60, 60, 80),
        "core": (200, 50, 30)
    }
    
    # Resource colors
    RESOURCE_COLORS = {
        "iron": (192, 192, 192),
        "copper": (184, 115, 51),
        "gold": (255, 215, 0),
        "crystal": (100, 200, 255),
        "artifact": (200, 100, 200)
    }
    
    # Game balance
    BASE_MINING_POWER = 1.0
    BASE_MINING_SPEED = 1.0  # Clicks per second
    DEPTH_SCALING = 1.15  # Resource scaling per depth level
    
    # Prestige
    PRESTIGE_DEPTH = 1000
    PRESTIGE_MULTIPLIER_BASE = 1.5
