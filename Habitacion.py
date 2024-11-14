import pygame
from Item import Item
import Utils
from Light_Sources import LightSource

# Clase para manejar los cuartos
class Habitacion:
    def __init__(self, nombre, imagen = None, items: Item = [], escalaImagen = 1, lista_luces = []) -> None:
        self.nombre = nombre;
        if (imagen is not None):
            self.imagen = Utils.get_imagen_cache(nombre_imagen=imagen)
            self.imagen = pygame.transform.scale(self.imagen, (self.imagen.get_width() * escalaImagen, self.imagen.get_height()*escalaImagen))
        self.items = items;
        
        self.luces = []
        for source in lista_luces:
            if len(source) > 2:
                self.luces.append(LightSource(source[0], source[1], source[2]))
            else:
                self.luces.append(LightSource(source[0], source[1]))
        pass

    def draw(self, enable = True):

        Utils.screen.fill(Utils.WHITE);
        Utils.screen.blit(self.imagen, (0,0))

        for item in self.items:
            item.draw(enable)
        pass