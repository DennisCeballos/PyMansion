import pygame
import Utils

# rect = [posX, posY, sizeX, sizeY]
class Item:
    def __init__(self, nombre, accion, col_puntos = [],
                 rect = [None], opacidad = 255, nombreImagen = None, escalaImagen = 1, color = None, tooltip = None) -> None:
        # Variables que se obtienen por argumentos
        self.nombre = nombre;
        
        self.imagen = None
        if (nombreImagen is not None):
            self.imagen = Utils.get_imagen_cache(nombre_imagen=nombreImagen)
            #self.imagen = pygame.transform.scale(self.imagen, (self.imagen.get_width() * escalaImagen, self.imagen.get_height()*escalaImagen))
            self.imagen = pygame.transform.scale(self.imagen, list(map(lambda x: x*escalaImagen, (self.imagen.get_width(), self.imagen.get_height()))))
        
        self.poligono = col_puntos;
        self.accion = accion;
        self.opacidad = opacidad;
        
        self.color = color if (color is not None) else 'green' # Setea el color a verde en caso no exista ningun color

        self.rect = None
        if rect[0] is not None:
            self.rect = pygame.Rect((rect[0], rect[1]), (rect[2], rect[3]))

        self.tooltip = nombre if (tooltip is None) else tooltip

        # Variables necesarias para el funcionamiento
        self.visible = True;
        self.enable = True;
        self.clicked = False;
        pass

    # Funcion para verificar que un punto pertenece al interior del poligono
    def point_in_polygon(self, point) -> bool:
        # Esto verifica que existe un rectangulo
        if self.rect is not None:
            # Si existe, entonces que retorne el calculo prefedinido por Pygame
            return self.rect.collidepoint(point)
        
        # Sino, que continue el calculo complicado
        num_vertices = len(self.poligono)
        x, y = point[0], point[1]
        inside = False
    
        # Store the first point in the polygon and initialize the second point
        p1 = self.poligono[0]
    
        # Loop through each edge in the polygon
        for i in range(1, num_vertices + 1):
            # Get the next point in the polygon
            p2 = self.poligono[i % num_vertices]
    
            # Check if the point is above the minimum y coordinate of the edge
            if y > min(p1[1], p2[1]):
                # Check if the point is below the maximum y coordinate of the edge
                if y <= max(p1[1], p2[1]):
                    # Check if the point is to the left of the maximum x coordinate of the edge
                    if x <= max(p1[0], p2[0]):
                        # Calculate the x-intersection of the line connecting the point to the edge
                        x_intersection = (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
    
                        # Check if the point is on the same line as the edge or to the left of the x-intersection
                        if p1[0] == p2[0] or x <= x_intersection:
                            # Flip the inside flag
                            inside = not inside
    
            # Store the current point as the first point for the next iteration
            p1 = p2
    
        # Return the value of the inside flag
        return inside

    # Dibujar el item  en pantalla
    def draw(self, enable = True):
        # Si existe un rectangulo, que lo dibuje
        if self.rect is not None:
            pygame.draw.rect(Utils.screen, self.color, self.rect, 0, 5)
        else:
            # Sino, es porque existe valores del poligono y hay que dibujarlo
            pygame.draw.polygon(Utils.screen, self.color, self.poligono)

        # Dibujar la imagen en pantalla, en caso no sea None
        if self.imagen is not None:
            if self.rect is not None:
                Utils.screen.blit(self.imagen, self.rect)
            else:
                Utils.screen.blit(self.imagen, (self.poligono[0][0]+20, self.poligono[0][1]+20))

        if enable:
            self.check_click()

    def check_click(self):
        ejecutar = False
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        
        if self.point_in_polygon(mouse_pos): # Verifica que el mouse este dentro del area del objeto
            # Dibujar el tooltip
            if self.tooltip is not None:
                tooltip = Utils.tooltip_Font.render(self.tooltip, False, (0,0,0) , (255,255,0))
                tooltip.set_alpha(180)
                Utils.screen.blit(tooltip, (mouse_pos[0]+16, mouse_pos[1]))

            if left_click == 1 and self.clicked == False:
                self.clicked = True
                ejecutar = True

            if left_click == 0:
                self.clicked = False

        if ejecutar: self.accion()
