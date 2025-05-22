import pygame
import sys
from Item import Item
import Utils
from Habitacion import Habitacion
from Examinable import Examinable, Tipo_Examinable
import pygame_gui
from Light_Sources import *
from TextManager import TextoManager
from InventarioManager import InventarioManager

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
def Accion_Imprimir_Pantalla(texto):
    if Utils.DEBUG: print("(En pantalla)" + texto)
    global hablando
    textoManager.lista_texto.append(texto)
    hablando = True

def Accion_Mover_habitacion(nombreHabitacion):
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

def Accion_Agregar_Item(item: Item, nombreHabitacion):
    global habitacion_actual

    if type(Item) is not Item:
        print("Agregar_Item: No ingresaste una variable de tipo Item")
        return
    
    for cuarto in habitaciones:
        if cuarto.nombre == nombreHabitacion:
            cuarto.items.append(item)
            return
        if Utils.DEBUG: print("Agregar_Item: No existe una habitacion con nombre ", nombreHabitacion)

def Accion_Examinar(x):
    # Logica para examinar un objeto en pantalla
    global inspeccionando
    global item_examinar
    global items_examinables

    if Utils.DEBUG: print("Examinando:" + str(x))
    
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
    tooltip="Empezar",
    accion = lambda x="Sala Principal": Accion_Mover_habitacion(x),
    col_rect = [200,500, 400, 100],
    color = (0, 0, 0),
    )

Puerta_SalaAtico = Item( "Ir Al aTiCo",
    accion= lambda x = "Atico": Accion_Mover_habitacion(x),
    col_rect = [190,100,55,60],
    nombreImagen = "Flecha_Ari.png",
    escalaImagen = 0.25,
    color = None
    )

Puerta_SalaEstudio = Item("Ir a Estudio",
    accion= lambda x="Estudio": Accion_Mover_habitacion(x),
    col_rect = [130, 400, 60, 55],
    nombreImagen = "Flecha_Izq.png",
    escalaImagen = 0.25,
    color = None,
    )

Puerta_SalaPatio = Item("Ir a Patio",
    accion= lambda x="Patio": Accion_Mover_habitacion(x),
    col_rect = [40, 570, 60, 55],
    nombreImagen = "Flecha_Izq.png",
    escalaImagen = 0.25,
    color = None,
    )

Puerta_SalaBodega = Item("Ir a Bodega",
    accion= lambda x="Sotano_base": Accion_Mover_habitacion(x),
    col_rect = [700, 570, 60, 55],
    nombreImagen = "Flecha_Der.png",
    escalaImagen = 0.25,
    color = None,
    )

Puerta_SalaHabitacion = Item("Ir a Habitacion",
    accion= lambda x="Habitacion": Accion_Mover_habitacion(x),
    col_rect = [610, 450, 60, 55],
    nombreImagen = "Flecha_Der.png",
    escalaImagen = 0.25,
    color = None,
    )

Puerta_EstudioSala = Item("Ir a Sala Principal",
    accion= lambda x="Sala Principal": Accion_Mover_habitacion(x),
    col_rect = [100, 700, 55, 60],
    nombreImagen = "Flecha_Abj.png",
    escalaImagen = 0.25,
    color= None
    )

Puerta_AbajoSala = Item("Ir a Sala Principal",
    accion= lambda x="Sala Principal": Accion_Mover_habitacion(x),
    col_rect = [400, 700, 55, 60],
    nombreImagen = "Flecha_Abj.png",
    escalaImagen = 0.25,
    color= None
    )

Flecha_BodegaDerecha = Item("Bodega derecha",
    tooltip="...",
    accion= lambda x="Sotano_Derecho": Accion_Mover_habitacion(x),
    col_rect = [480, 410, 60, 55],
    nombreImagen = "Flecha_Der.png",
    escalaImagen = 0.25,
    color = None,
    )

Flecha_BodegaIzquierda = Item("Bodega Izquierda",
    tooltip = "...",
    accion= lambda x="Sotano_Izquierdo": Accion_Mover_habitacion(x),
    col_rect = [210, 410, 60, 55],
    nombreImagen = "Flecha_Izq.png",
    escalaImagen = 0.25,
    color = None,
    )

Flecha_BodegaAbajo = Item("Bodega Base", 
    tooltip = "Volver a bodega principal",
    accion= lambda x="Sotano_base": Accion_Mover_habitacion(x),
    col_rect = [400, 700, 55, 60],
    nombreImagen = "Flecha_Abj.png",
    escalaImagen = 0.25,
    color= None
    )

CajaFuerte = Item("Caja de seguridad",
    accion= lambda x="Aass": Accion_Examinar(x),
    col_rect=[580, 600, 112, 78],
    nombreImagen = "Caja_seguridad.png",
    escalaImagen = 0.75,
    color=None)

FotoHabitacion = Item("Fotografia",
    accion= lambda x="Es una foto del dueno de la mansion: alBerT CaMUs": Accion_Imprimir_Pantalla(x),
    col_rect=[225, 450, 40, 55],
    nombreImagen = None,
    color = None
    )

## * DEFINICION DE ITEMS EXAMINABLES *
items_examinables = [
    Examinable("Caja seguridad",
               Tipo_Examinable.Puzzle,
               texto="Ingresa la contrasena",
               accion_puzzle=lambda x: Accion_Agregar_Item(Puerta_SalaAtico,"Sala Principal"),
               puzzleAns="BTCMS"
               ),
    
    Examinable("RespuestaPergamino",
               Tipo_Examinable.Imagen,
               texto="...",
               imagen = "Pergamino.png",
               escalaImagen=0.1
               )
]

## * DEFINICION DE HABITACIONES
habitaciones = [
    Habitacion("Inicio",
               items = [Puerta_InicioSala],
               imagen = "nas",
               escalaImagen = 1,
               ),

    Habitacion("Sala Principal",
               items = [Puerta_SalaEstudio, Puerta_SalaPatio, Puerta_SalaBodega, Puerta_SalaHabitacion],
               imagen= "Habitacion_Sala.jpg",
               escalaImagen = 0.4,
               lista_luces = [ (80, 400), (685,415),  (600,420, 50), (385,185, 50), (385, 415, 50), (390, 490, 50), (635, 180, 50), (175,135, 50), (520,425, 30), (250, 420, 30)]
            ),   
    
    Habitacion("Patio",
               items=[Puerta_AbajoSala],
               imagen= "Habitacion_Patio_Closed.png",
               escalaImagen=0.68,
               lista_luces = [ (620, 565, 80), (255,530, 60), (555, 470, 40), (290, 480, 30)]
            ),

    Habitacion("Estudio",
               items = [Puerta_EstudioSala],
               imagen = "Habitacion_Estudio.jpg",
               escalaImagen = 0.4,
               lista_luces = [ (155,375,140), (245,275,40) ]
            ),

    Habitacion("Habitacion",
               items = [Puerta_AbajoSala, CajaFuerte, FotoHabitacion],
               imagen= "Habitacion_Habitacion.jpg",
               escalaImagen = 0.4,
               lista_luces = [ (235,265, 60), (700,400,160), (300,405,60), (75,485,70)]
            ),

    Habitacion("Atico",
               items = [Puerta_AbajoSala],
               imagen= "Habitacion_Atico.jpg",
               escalaImagen = 1.125,
            ),
    
    Habitacion("Sotano_base",
               items=[Puerta_AbajoSala, Flecha_BodegaDerecha, Flecha_BodegaIzquierda],
               imagen = "Habitacion_Sotano-Bas.jpg",
               escalaImagen = 0.4,
               lista_luces = [ (85,315,160), (630,375), (380,425,50), (250,525), (605,655) ]
            ),

    Habitacion("Sotano_Derecho",
               items=[Flecha_BodegaAbajo],
               imagen = "Habitacion_Sotano-Der.jpg",
               escalaImagen = 0.4,
               lista_luces = [ (75,565,110), (120,365,120), (760,410,120), (350,350,120) ]
            ),
            
    Habitacion("Sotano_Izquierdo",
               items=[Flecha_BodegaAbajo],
               imagen = "Habitacion_Sotano-Izq.jpg",
               escalaImagen = 0.4,
               lista_luces = [ (40,210,50), (60,360,50), (725,240,50), (485,360,120)]
            ),
]

## * FIN DE MODIFICACIONES

transicionando = False
fade_counter = 0


inspeccionando = False
# Generar un item examinable de error
item_examinar = Examinable("Error",
                tipo = Tipo_Examinable.Nota,
                texto = "Estas mirando un error, no se encontro el nombre del item examinable"
                )

hablando = False

textoManager = TextoManager()
light_manager = LightManager()
inventarioManager = InventarioManager()

# Variables de uso durante el juego
inventario = []  # Para almacenar objetos del inventario
habitacion_actual: Habitacion = habitaciones[1]  # Habitacion de inicio
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
    global hablando

    inventarioManager.agregarItem(Puerta_AbajoSala)

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


        # Si es que se esta analizando, el cuarto no deberia ser interactuable
        if not transicionando:
            # Dibujar el cuarto actual
            habitacion_actual.draw(enable = not (inspeccionando or hablando or transicionando)  )
            # Dibujar el efecto linterna y las luces
            light_manager.draw()
            # Dibujar el inventario
            inventarioManager.draw()
            inventarioManager.update()

        if inspeccionando == True:
            # Se dibuja la interfaz del item examinandose
            item_examinar.draw()
            # Se actuliza valor de inspeccionando de acuerdo al item examinar actual
            inspeccionando = item_examinar.activo

        if hablando == True:
            # Logica para generar texto en pantalla
            textoManager.draw()
            hablando = textoManager.update()


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

