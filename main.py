import pygame
import sys
from Item import Item
import Utils
from Habitacion import Habitacion
from Examinable import Examinable, Tipo_Examinable
import pygame_gui
import random
import math

# Inicializar juego
pygame.init()

timer = pygame.time.Clock()

# Dimensiones de la pantalla
Utils.screen = pygame.display.set_mode((Utils.ANCHO, Utils.ALTO))
pygame.display.set_caption('Pyjuego d\'Misterio')


# Fuentes
Utils.font = pygame.font.Font(None, 36)
Utils.tooltip_Font = pygame.font.Font(None, 26)
Utils.dialogue_Font = pygame.font.Font(None, 30)
Utils.tittle_Font = pygame.font.Font(None, 35)

# Pygame_ui
Utils.Manager_Ui = pygame_gui.UIManager((Utils.ANCHO, Utils.ALTO))

#* ACCIONES
#*
# Definir los "game Objects" (objetos que aparecen en el juego)
def Imprimir_Pantalla(texto):
    if Utils.DEBUG: print("(En pantalla)" + texto)
    global hablando
    textoManager.text_actual = texto
    hablando = True


def Mover_habitacion(nombreHabitacion):
    global transicionando
    global habitacion_actual # Es necesario que sea global para que acceda a la variable del juego
    
    cuartoObjetivo = habitacion_actual
    if Utils.DEBUG: print("Accion: Moviendo a la habitacion " + nombreHabitacion)
    
    transicionando = True

    # Buscar entre todas las habitaciones
    for cuarto in habitaciones:
        if cuarto.nombre == nombreHabitacion:
            cuartoObjetivo = cuarto # Guardar la habitacion a la cual se va mover

    if Utils.DEBUG and cuartoObjetivo == habitacion_actual: print("Error_Accion: No se encontro una habitacion de nombre " + nombreHabitacion)

    habitacion_actual = cuartoObjetivo

def Examinar(x):
    # Logica para examinar un objeto en pantalla
    global inspeccionando
    global item_examinar
    global items_examinables

    if Utils.DEBUG: print("Examinando:" + str(x))
    
    # Generar un item examinable de error
    item_examinar = Examinable("Error",
                    tipo="Nota",
                    texto="Estas mirando un error, no se encontro el nombre del item examinable"
                    ),
    
    for i in items_examinables:
        if i.nombre == str(x):
            item_examinar = i
        
    inspeccionando = True
    pass

### *** Pasos para disenar el juego ***
# * 1. DEFINIR LOS ITEMS QUE APARECEN EN EL JUEGO
# *
# * 2. DEFINIR LOS ITEMS_EXAMINABLES (y vinvularlos a los items)
# *
# * 3. AGREGAR LOS ITEMS A LAS HABITACIONES
# *
### *** 

## * DEFINICION DE ITEMS
pintura_sala = Item("Pintura",
                    col_puntos = [[100,100], [100,200], [300,300], [200,100]],
                    accion = lambda x="Esta es una pintura": Imprimir_Pantalla(x),
                    nombreImagen = "object.png"
                    )


puerta_Estudio = Item("Puerta Estudio",
                      col_puntos= [ [Utils.ANCHO-200, Utils.ALTO-550], [Utils.ANCHO, Utils.ALTO-550], [Utils.ANCHO, Utils.ALTO], [Utils.ANCHO-200,Utils.ALTO] ],
                      accion = lambda x="Estudio": Mover_habitacion(x)
                      )

laptop = Item("Laptop",
              rect = [ Utils.ANCHO/2, Utils.ALTO/2, 120, 80],
              accion = lambda x="Esta es una laptop muy antigua y que deberia de irse a la basura": Imprimir_Pantalla(x)
              )

celular = Item("Celular",
               col_puntos = [[Utils.ANCHO/2-200-20, Utils.ALTO/2-200-20], [Utils.ANCHO/2-200+20, Utils.ALTO/2-200-20], [Utils.ANCHO/2-200+20, Utils.ALTO/2-200+20], [Utils.ANCHO/2-200-20, Utils.ALTO/2-200+20]],
               accion = lambda x="Un iphone": Imprimir_Pantalla(x))

puerta_SalaPrincipal = Item("Puerta Sala Principal",
                            rect = [200, 550, 200, 500,],
                            accion = lambda x="Sala Principal": Mover_habitacion(x)
                            )

notaPequena = Item("Notita",
                   rect = [ Utils.ANCHO/2 - 30, Utils.ALTO/2-100, 100, 100 ],
                   accion = lambda x="Nota rara": Examinar(x)
                   )


## * DEFINICION DE ITEMS EXAMINABLES *
items_examinables = [
    Examinable("Nota rara",
                    tipo="Puzzle",
                    texto="Estas mirando un objeto raro",
                    imagen="caja.png",
                    escalaImagen = 0.4,
                    ),
]

## * DEFINICION DE HABITACIONES
habitaciones = [
    Habitacion("Sala Principal",
               items = [pintura_sala, puerta_Estudio, celular, notaPequena],
               imagen= "Habitacion_Sala.jpg",
               escalaImagen = 0.4
               ),   

    Habitacion("Estudio",
               items = [laptop, puerta_SalaPrincipal, notaPequena],
               imagen= "Habitacion_Estudio.jpg",
               escalaImagen = 0.4
               ),
]

## * FIN DE MODIFICACIONES

transicionando = False
fade_counter = 0

# Variables de uso durante el juego
inventario = []  # Para almacenar objetos del inventario
habitacion_actual = habitaciones[0]  # Habitacion de inicio

inspeccionando = False
item_examinar = False # debe cambiarse a un item

hablando = False

class TextoManager():
    def __init__(self):
        self.text_actual = ""
        self.text_counter = 0
        self.text_speed = 2
        self.text_finalizado = False
        self.text_clicked = False
        pass

    def draw(self):
        global hablando

        fondo_texto = pygame.rect.Rect((0, Utils.ALTO-300), (Utils.ANCHO, 300))
        pygame.draw.rect( Utils.screen, 'black', fondo_texto )
        
        if self.text_counter < self.text_speed * len(self.text_actual):
            self.text_counter += 1
        elif ( self.text_counter >= self.text_speed * len(self.text_actual) ):
            self.text_finalizado = True
            # Resetear las variables

        snip = Utils.font.render(self.text_actual[0:self.text_counter // self.text_speed], True, 'white')
        Utils.screen.blit(snip, (0+10, Utils.ALTO-300+10))

        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        if fondo_texto.collidepoint(mouse_pos): # Verifica que el mouse este dentro del rango del objeto
            # Si se hace click antes de qe termine, que se adelante el final
            if left_click == 1 and self.text_clicked == False:
                self.text_clicked = True
                self.text_counter = self.text_speed * len(self.text_actual)
                # Si ya termino, que se cierre la ventana
                if self.text_finalizado:
                    self.text_finalizado = False
                    hablando = False
                    self.text_counter = 0

            if left_click == 0:
                self.text_clicked = False




linterna = Utils.get_imagen_cache("flashlight.png")
linterna = pygame.transform.scale(linterna, list(map(lambda x: x*1, linterna.size)))

# FireLight class
class PulsatingLight:
    def __init__(self, x, y, max_radius):
        self.x = x
        self.y = y
        self.max_radius = max_radius
        self.base_radius = max_radius * 0.9
        self.pulse_speed = 0.003  # Speed of pulsation
        self.time_offset = random.uniform(0, 2 * math.pi)  # Randomize phase for variation

    def draw(self, surface):
        # Calculate pulsating radius
        pulse = (math.sin(pygame.time.get_ticks() * self.pulse_speed + self.time_offset) + 1) / 2
        current_radius = self.base_radius + pulse * (self.max_radius - self.base_radius)

        # Draw multiple layers with increasing alpha closer to the center
        num_layers = 2
        for i in range(num_layers, 0, -1):
            # Increase alpha for inner layers (closer to 255)
            alpha = int(240 + 15 * (i / num_layers))
            color = (*(0,0,0), alpha)  # Apply transparency
            
            # Inner layers have a higher radius ratio (sharper glow inside)
            layer_radius = int(current_radius * (i / num_layers*2 + 0.2))

            # Create a surface for each circle with transparency
            circle_surf = pygame.Surface((layer_radius * 2, layer_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surf, color, (layer_radius, layer_radius), layer_radius)

            filter = pygame.surface.Surface((Utils.ANCHO, Utils.ALTO))
            filter.fill((50,50,50))
            
            filter.blit(linterna, list(map(lambda x: x-linterna.size[0]/2, pygame.mouse.get_pos())))
            # Blit each layer at the light's position
            filter.blit(circle_surf, (self.x - layer_radius, self.y - layer_radius))#, special_flags=pygame.BLEND_RGBA_SUB)
            
            Utils.screen.blit(filter, (0,0), special_flags=pygame.BLEND_RGB_SUB)



# Main funcion que ejecuta el juego
def main():
    global habitacion_actual
    global inspeccionando
    global transicionando
    global item_examinar
    global fade_counter

    # Ocultar el puntero
    if not Utils.DEBUG:
        pygame.mouse.set_cursor( pygame.SYSTEM_CURSOR_CROSSHAIR )

    light_source = PulsatingLight(80, Utils.ALTO // 2 , 40)  # Light position and max radius

    global textoManager
    textoManager = TextoManager()

    # Main game loop
    running = True
    while running:
        UI_REFRESH_RATE = pygame.time.Clock().tick(60)/1000
        timer.tick(60)

        # Dibujar el cuarto actual
        # Si es que se esta analizando, el cuarto no deberia ser interactuable
        if not transicionando:
            habitacion_actual.draw(enable = not (inspeccionando or hablando or transicionando)  )

        if inspeccionando == True:
            # Se dibuja la interfaz del item examinandose
            item_examinar.draw()
            # Se actuliza valor de inspeccionando de acuerdo al item examinar actual
            inspeccionando = item_examinar.activo

        if hablando == True:
            # Logica para generar texto en pantalla
            textoManager.draw()

        # Manejar los eventos del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            Utils.Manager_Ui.process_events(event)

        Utils.Manager_Ui.update(UI_REFRESH_RATE)

        Utils.Manager_Ui.draw_ui(Utils.screen)

        #! THIS WORKS AND ITS COOL, BUT MUST BE CHANGED
        if transicionando:
            if fade_counter < 255:
                fade_counter += 25
                fade = pygame.Surface((Utils.ANCHO, Utils.ALTO))
                fade.fill((0,0,0))
                fade.set_alpha(fade_counter)
                Utils.screen.blit(fade, (0,0))
            else:
                transicionando = False
                fade_counter = 0
        
        
        # Dibujar el efecto linterna
        light_source.draw(Utils.screen)

        # posicion del mouse
        mouse_pos_screen = pygame.mouse.get_pos()
        
        # Dibujar el tooltip de posicion del mouse
        if Utils.DEBUG and pygame.mouse.get_focused():
            tooltip = Utils.tooltip_Font.render(str(mouse_pos_screen), False, (0,0,0) , (0,255,255))
            tooltip.set_alpha(180)
            Utils.screen.blit(tooltip, (mouse_pos_screen[0] - tooltip.size[0] - 10, mouse_pos_screen[1]+10 ))

        # Actualizar el display del juego (???)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

