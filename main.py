import pygame
import sys
from Item import Item
import Utils
from Habitacion import Habitacion
from Examinable import Examinable, Tipo_Examinable
import pygame_gui
import random
import math
from Light_Sources import *
from TextManager import TextoManager

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
    textoManager.lista_texto.append(texto)
    textoManager.lista_texto.append("Lo lgramos")
    hablando = True


def Mover_habitacion(nombreHabitacion):
    global transicionando
    global habitacion_actual # Es necesario que sea global para que acceda a la variable del juego
    global lightManager
    
    cuartoObjetivo = habitacion_actual
    if Utils.DEBUG: print("Accion: Moviendo a la habitacion " + nombreHabitacion)
    
    transicionando = True

    # Buscar entre todas las habitaciones
    for cuarto in habitaciones:
        if cuarto.nombre == nombreHabitacion:
            cuartoObjetivo = cuarto # Guardar la habitacion a la cual se va mover

    if Utils.DEBUG and cuartoObjetivo == habitacion_actual: print("Error_Accion: No se encontro una habitacion de nombre " + nombreHabitacion)

    habitacion_actual = cuartoObjetivo
    light_manager.lights = habitacion_actual.luces

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
Puerta_InicioSala = Item( "Puerta_Inicio-Sala",
    tooltip="",
    accion = lambda x="Sala Principal": Mover_habitacion(x),
    rect = [200,500, 400, 100],
    color = (0, 0, 0),
    )

Puerta_SalaEstudio = Item( "Puerta_Sala",
                          tooltip = "Ir a Estudio",
                          accion= lambda x="Estudio": Mover_habitacion(x),
                          rect = [130, 400, 60, 50],
                          nombreImagen = "Flecha_Izq.png",
                          escalaImagen = 0.25,
                          color = None,
                          ) 

## * DEFINICION DE ITEMS EXAMINABLES *
items_examinables = [
    

]

## * DEFINICION DE HABITACIONES
habitaciones = [
    Habitacion("Inicio",
               items = [Puerta_InicioSala],
               imagen = "nas",
               escalaImagen = 1,
               ),

    Habitacion("Sala Principal",
               items = [Puerta_SalaEstudio],
               imagen= "Habitacion_Sala.jpg",
               escalaImagen = 0.4,
               lista_luces = [ (80, 400), (685,415),  (600,420, 50), (385,185, 50), (385, 415, 50), (390, 490, 50), (635, 180, 50), (175,135, 50), (520,425, 30), (250, 420, 30)]
            ),   
    
    Habitacion("Patio",
               items=[],
               imagen= "Habitacion_Patio.jpg",
               escalaImagen=0.68,
               lista_luces = [ (620, 565, 60), (255,530, 40), (555, 470, 20), (290, 480, 10)]
            ),

    Habitacion("Estudio",
               items = [],
               imagen = "Habitacion_Estudio.jpg",
               escalaImagen = 0.4,
               lista_luces = []
            ),

    Habitacion("Habitacion",
               items = [],
               imagen= "Habitacion_Habitacion.jpg",
               escalaImagen = 0.4,
            ),

    Habitacion("Atico",
               items = [],
               imagen= "Habitacion_Atico.jpg",
               escalaImagen = 1.125,
            ),
    
    Habitacion("Sotano_base",
               items=[],
               imagen = "Habitacion_Sotano-Bas.jpg",
               escalaImagen = 0.4
            ),

    Habitacion("Sotano_Derecho",
               items=[],
               imagen = "Habitacion_Sotano-Der.jpg",
               escalaImagen = 0.4
            ),
            
    Habitacion("Sotano_Izquierdo",
               items=[],
               imagen = "Habitacion_Sotano-Izq.jpg",
               escalaImagen = 0.4
            ),
]

## * FIN DE MODIFICACIONES

transicionando = False
fade_counter = 0


inspeccionando = False
item_examinar = False # debe cambiarse a un item

hablando = False

textoManager = TextoManager()
light_manager = LightManager()

# Variables de uso durante el juego
inventario = []  # Para almacenar objetos del inventario
habitacion_actual = habitaciones[0]  # Habitacion de inicio
light_manager.lights = habitacion_actual.luces

# Main funcion que ejecuta el juego
def main():
    global habitacion_actual
    global inspeccionando
    global transicionando
    global item_examinar
    global fade_counter
    global light_manager
    global textoManager

    # Ocultar el puntero
    if not Utils.DEBUG:
        pygame.mouse.set_cursor( pygame.SYSTEM_CURSOR_CROSSHAIR )

    # Main game loop
    running = True
    while running:
        UI_REFRESH_RATE = pygame.time.Clock().tick(60)/1000
        timer.tick(60)

        # Manejar los eventos del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if Utils.DEBUG:
                    print(f"Pos: {pygame.mouse.get_pos()}")

            Utils.Manager_Ui.process_events(event)


        # Dibujar el cuarto actual
        # Si es que se esta analizando, el cuarto no deberia ser interactuable
        if not transicionando:
            habitacion_actual.draw(enable = not (inspeccionando or hablando or transicionando)  )
            # Dibujar el efecto linterna y las luces
            light_manager.draw()

        if inspeccionando == True:
            # Se dibuja la interfaz del item examinandose
            item_examinar.draw()
            # Se actuliza valor de inspeccionando de acuerdo al item examinar actual
            inspeccionando = item_examinar.activo

        if hablando == True:
            # Logica para generar texto en pantalla
            textoManager.draw()
            textoManager.update()


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

