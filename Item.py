import pygame
import Utils

# rect = [posX, posY, sizeX, sizeY]
class Item:
    def __init__(self, nombre, accion,
                 col_rect = [None], col_puntos = [None], nombreImagen = None, escalaImagen = 1.0,
                 opacidad = 255, color = None, tooltip = None) -> None:
        # Variables que se obtienen por argumentos
        self.nombre = nombre
        self.accion = accion
        self.opacidad = opacidad
        self.nombreImagen = nombreImagen
        
        alpha = 255 if Utils.DEBUG else 0
        self.color = (127,255,0, alpha) if (color is None) else color #, 0) # Setea el color a verde en caso no exista ningun color


        # Creacion de la superficie que cubre todo el escenario y servira para ubicar los nuevos items
        self.superficie_type = ""
        self.superficie = pygame.surface.Surface((Utils.ANCHO, Utils.ALTO), pygame.SRCALPHA) #se genera de forma transparente

        self.rect = None
        # Si es que se ha dado la info para un rect
        if col_rect[0] is not None:
            self.rect = pygame.Rect((col_rect[0], col_rect[1]), (col_rect[2], col_rect[3]))
            
            # Se guarda ls superficie como un rectangulo
            pygame.draw.rect(self.superficie, color=self.color, rect=col_rect)
            self.superficie_type = "rect"

        # Si es que se ha dado la info para un polygono
        if col_puntos[0] is not None:
            # Se guarda ls superficie como un poligono
            pygame.draw.polygon(self.superficie, color=self.color, points=col_puntos)
            self.superficie_type = "polygon"
            # se guarda los puntos en un objeto
            self.poligono = [x for x in col_puntos]

        # Se guarda la informacion del tooltip que se da (se asigna por defecto el nombre del propio item)
        self.tooltip = nombre if (tooltip is None) else tooltip

        # Variables necesarias para el funcionamiento
        self.visible = True;
        self.enable = True;
        self.clicked = False;

        # Si es que se ha dado la info de una imagen
        if nombreImagen is not None:
            self.imagen = Utils.get_imagen_cache(nombre_imagen=nombreImagen)
            self.imagen = pygame.transform.scale(self.imagen, list(map(lambda x: x*escalaImagen, (self.imagen.get_width(), self.imagen.get_height()))))
            if col_rect[0] is not None:
                self.superficie.blit(self.imagen, (col_rect[0], col_rect[1]))
            if col_puntos[0] is not None:
                self.superficie.blit(self.imagen, col_puntos[0])

        pass

    # Funcion para verificar que un punto pertenece al interior del poligono
    def point_in_polygon(self, point) -> bool:
        # Esto verifica que existe un rectangulo
        if self.rect is not None:
            # Si existe, entonces que retorne el calculo prefedinido por Pygame
            return self.rect.collidepoint(point)
        
        print("Hola estoy en el error")
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
        Utils.screen.blit(self.superficie, self.superficie.get_rect())

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
