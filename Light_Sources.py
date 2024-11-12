import pygame
import Utils
import random
import math

# Por el momento, solo velas
class LightSource:
    def __init__(self, x, y, max_radius = 80):
        self.x = x
        self.y = y
        self.max_radius = max_radius
        self.base_radius = max_radius * 0.9
        self.pulse_speed = random.uniform(0.001, 0.004)  # Speed of pulsation
        self.time_offset = random.uniform(0, 2 * math.pi)  # Randomize phase for variation

    def get_current_radius(self):
        pulse = (math.sin(pygame.time.get_ticks() * self.pulse_speed + self.time_offset) + 1) / 2
        return self.base_radius + pulse * (self.max_radius - self.base_radius)

class LightManager:
    def __init__(self):
        linterna = Utils.get_imagen_cache("flashlight.png")
        self.linterna = pygame.transform.scale(linterna, list(map(lambda x: x*1, linterna.size)))

        self.lights: list[LightSource] = []

        self.filter = pygame.surface.Surface((Utils.ANCHO, Utils.ALTO))
        self.opacidad = 180 # Valor de 0 a 255

    def draw(self):
        
        self.filter.fill((self.opacidad,self.opacidad,self.opacidad))
        
        for light in self.lights:

            # Calculate pulsating radius
            current_radius = light.get_current_radius()

            # Draw multiple layers with increasing alpha closer to the center
            num_layers = 3
            for i in range(num_layers, 0, -1):
                
                al = [255,180,90]
                alpha = int(180 * ( (-i+num_layers) / num_layers +0.5))
                color = (*(0,0,0), alpha)  # Apply transparency
                
                # Inner layers have a higher radius ratio (sharper glow inside)
                layer_radius = int(current_radius * (i / num_layers + 0.5))

                # Create a surface for each circle with transparency
                circle_surf = pygame.Surface((layer_radius * 2, layer_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(circle_surf, color, (layer_radius, layer_radius), layer_radius)
                
                self.filter.blit(circle_surf, (light.x - layer_radius, light.y - layer_radius))#, special_flags=pygame.BLEND_RGBA_SUB)
            
            
        self.filter.blit(self.linterna, list(map(lambda x: x-self.linterna.size[0]/2, pygame.mouse.get_pos())))
        
        # Blit each layer at the light's position    
        Utils.screen.blit(self.filter, (0,0), special_flags=pygame.BLEND_RGB_SUB)

