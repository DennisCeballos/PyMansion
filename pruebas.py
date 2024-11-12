import pygame
import random
import Utils
import math

pygame.init()

timer = pygame.time.Clock()

Utils.screen = pygame.display.set_mode((Utils.ANCHO, Utils.ALTO))
Utils.font = pygame.font.Font(None, 36)
Utils.tooltip_Font = pygame.font.Font(None, 26)

linterna = Utils.get_imagen_cache("flashlight.png")
linterna = pygame.transform.scale(linterna, list(map(lambda x: x*1, linterna.size)))

class LightSource:
    def __init__(self, x, y, max_radius):
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
        self.lights: list[LightSource] = []

        self.filter = pygame.surface.Surface((Utils.ANCHO, Utils.ALTO))
        self.opacidad = 200 # Valor de 0 a 255

    def draw(self):
        
        self.filter.fill((self.opacidad,self.opacidad,self.opacidad))
        
        for light in self.lights:

            # Calculate pulsating radius
            current_radius = light.get_current_radius()

            # Draw multiple layers with increasing alpha closer to the center
            num_layers = 4
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
            
            
        self.filter.blit(linterna, list(map(lambda x: x-linterna.size[0]/2, pygame.mouse.get_pos())))
        
        # Blit each layer at the light's position    
        Utils.screen.blit(self.filter, (0,0), special_flags=pygame.BLEND_RGB_SUB)



# Main funcion que ejecuta el juego
def main():

    # Ocultar el puntero
    imagen = Utils.get_imagen_cache("Habitacion_Sala.png")

    light_manager = LightManager()  # Light position and max radius
    light_manager.lights.append(LightSource(80, Utils.ALTO // 2, 80))
    light_manager.lights.append(LightSource(Utils.ALTO // 2, 80, 10))

    running = True
    while running:
        timer.tick(60)

        # Manejar los eventos del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        Utils.screen.fill(Utils.WHITE);
        Utils.screen.blit(imagen, (0,0))
        
        # Dibujar el efecto linterna y las luces
        light_manager.draw()

        # posicion del mouse
        mouse_pos_screen = pygame.mouse.get_pos()
        
        # Dibujar el tooltip de posicion del mouse
        if Utils.DEBUG and pygame.mouse.get_focused():

            tooltip = Utils.tooltip_Font.render(str(mouse_pos_screen) + str(Utils.screen.get_at(mouse_pos_screen)) + str(Utils.screen.get_alpha()), False, (0,0,0) , (0,255,255))
            tooltip.set_alpha(180)
            Utils.screen.blit(tooltip, (mouse_pos_screen[0], mouse_pos_screen[1]+10 ))

        # Actualizar el display del juego (???)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
