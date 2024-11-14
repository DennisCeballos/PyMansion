import pygame
import Utils
from Item import Item
import math

class InventarioManager():
    def __init__(self):
        self.lista_items: list[Item] = []
        self.alto_fondo = 50
        self.fondo_inventario = pygame.rect.Rect((0,Utils.ALTO-self.alto_fondo), (Utils.ANCHO, self.alto_fondo))
        self.fondo_clicked = False
        pass

    def draw(self):
        pygame.draw.rect( Utils.screen, (28, 44, 66), self.fondo_inventario )
        for it in self.lista_items:
            it.draw()
    
    def agregarItem(self, item: Item):
        rectPos = pygame.rect.Rect( len(self.lista_items)* self.alto_fondo + 10, Utils.ALTO - self.alto_fondo, self.alto_fondo, self.alto_fondo)
        nuevoAdaptado = Item(item.nombre, item.accion, rectPos, nombreImagen=item.nombreImagen, escalaImagen = item.imagen.get_rect().width/item.imagen.get_rect().width*self.alto_fondo, color=(0,0,0) )
        
        self.lista_items.append(nuevoAdaptado)


    def update(self):        
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        if self.fondo_inventario.collidepoint(mouse_pos): # Verifica que el mouse este dentro del rango del objeto
            # Si se hace click antes de qe termine, que se adelante el final
            if left_click == 1 and self.fondo_clicked == False:
                self.fondo_clicked = True
                numeroElegido = math.floor( (mouse_pos[0]-10)/50 )
                
                if len(self.lista_items) >= numeroElegido+1:
                    self.lista_items[numeroElegido].accion() 

            if left_click == 0:
                self.fondo_clicked = False

