import pygame
from Item import Item
import Utils

# Clase para manejar los cuartos
class Habitacion:
    def __init__(self, nombre, imagen = None, items: Item = [], escalaImagen = 1) -> None:
        self.nombre = nombre;
        if (imagen is not None):
            self.imagen = Utils.get_imagen_cache(nombre_imagen=imagen)
            self.imagen = pygame.transform.scale(self.imagen, (self.imagen.get_width() * escalaImagen, self.imagen.get_height()*escalaImagen))
        self.items = items;
        pass

    def draw(self, enable = True):

        Utils.screen.fill(Utils.WHITE);
        Utils.screen.blit(self.imagen, (0,0))

        for item in self.items:
            item.draw(enable)
        pass