import sys
import math
import random
import pygame as pg 

pg.init() # initializes pygame

# defining color table
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LT_GRAY = (180, 180, 180)
GRAY =(120, 120, 120)
DK_GRAY = (80, 80, 80)

class Particle(pg.sprite.Sprite):
    """Builds ejection particles for simulation"""

    gases_colors = {'SO2': LT_GRAY, 'CO2': GRAY, 'H2S': DK_GRAY, 'H2O': WHITE}

    VENT_LOCATION_XY = (320, 300) # launch point for particles
    IO_SURFACE_Y = 308
    GRAVITY = 0.5 # pixels per frame, added to dy each game loop
    VELOCITY_SO2 = 8 # pixels per frame

    # scalars SO2 atomic weight / particle atomic weight, used for velocity
    vel_scalar = {'SO2': 1, 'CO2': 1.45, 'H2S': 1.9, 'H2O': 3.6}

# defining a constructor method for the particle object
    def __init__(self, screen, background):
        super().__init()
        self.screen = screen
        self.background = background
        self.image = pg.Surface((4, 4)) # assigns particle image to Surface object & makes it square with 4 pixel length sides
        self.rect = self.image.get_rect()
        self.gas = random.choice(list(Particle.gases_colors.keys())) # randomly chooses particle type from the keys in gases_color dictionary
        self.color = Particle.gases_colors[self.gas] # gets correct color of the gas chosen
        self.vel = Particle.VELOCITY_SO2 * Particle.vel_scalar[self.gas] # determines velocity of chosen gas
        self.x, self.y = Particle.VENT_LOCATION_XY
        self.vector() # calculates the particle's motion vector

    def vector(self):
        """Calculate particle vector at launch point."""
        orient = random.uniform(60, 120) # 90 is vertical, randomly chooses launch direction cuz volcanoes spew out in all directions
        radians = math.radians(orient)
        self.dx = self.vel * math.cos(radians)
        self.dy = -self.vel * math.sin(radians)
    
    def update(self):
        """Apply gravity, draw path, & handle boundary conditions"""
        self.dy += Particle.GRAVITY
        pg.draw.line(self.background, self.color,(self.x, self.y), # draws a line behind the particle
                        (self.x + self.dx, self.y + self.dy))
        self.x += self.dx
        self.y += self.dy 

        if self.x < 0 or self.x > self.screen.get_width(): # if particle reaches the edges, takes the particle out
            self.kill()
        if self.y < 0 or self.y > Particle.IO_SURFACE_Y:
            self.kill()

def main():
    """Set up & run game screen & loop"""
    screen = pg.display.set_mode((639, 360))
    pg.display.set_caption("IO Volcano Simulator")
    background = pg.image.load('tvashtar_plume.gif') # sets the background to an image
    