import pygame
import sys
from enum import Enum
from Item import Item
import Utils

DEBUG = True

# Inicializar juego
pygame.init()

timer = pygame.time.Clock()

# Dimensiones de la pantalla
ANCHO, ALTO = 900, 700
Utils.screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Pyjuego d\'Misterio')

# Colores guardados globalmente
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Cargar imagenes
cache_imagenes = {}
# Recibe la direccion de la imagen
def get_imagen_cache(nombre_imagen: str) -> pygame.image:
    if not nombre_imagen in cache_imagenes:
        try:
            cache_imagenes[nombre_imagen] = pygame.image.load(nombre_imagen)
        except Exception:
            print("!!ERROR: no hay un archivo de imagen con ese nombre")
    return cache_imagenes[nombre_imagen]

# Fuentes
Utils.font = pygame.font.Font(None, 36)
Utils.tooltip_Font = pygame.font.Font(None, 26)
Utils.dialogue_Font = pygame.font.Font(None, 30)
Utils.tittle_Font = pygame.font.Font(None, 35)

# Clase para manejar los objetos


# Clase para definir los UNICOS tipos de items examinalbes
class Tipo_Examinable(Enum):
    Nota = 0
    Imagen = 1
    Puzzle = 2

#! Pueden existir (por ahora) solo tipos "Imagen", "Nota", "Puzzle"
class Item_Examinable:
    def __init__(self, nombre, tipo: Tipo_Examinable, imagen = "Imagenes/error404.png", texto = "No haz asignado ningun texto"):
        self.nombre = nombre
        self.tipo = tipo
        self.imagen = imagen
        self.texto = texto
        self.activo = True
        self.btn_regresar = Item("Regresar ...", rect= [ANCHO/2-200, ALTO-50, 400, 100], accion = self.cambiar_Activo, color=(40, 40, 40))
        
        if tipo == "Imagen":
            # Logica para renderizar la imagen
            self.imagen = get_imagen_cache(self.imagen)
        
        elif tipo == "Nota":
            self.texto = Utils.tooltip_Font.render(texto, False, (0,0,0))
        
        elif tipo == "Puzzle":
            pass
    
    # Funcion para la lambda
    def cambiar_Activo(self):
        self.activo = False

    def draw(self):
        self.activo = True #asumimos, por definicion, que si lo quisiste dibujar, es porque quieres activarlo

        # Dibujar capa negra transparente encima
        s = pygame.Surface((ANCHO, ALTO))
        s.set_alpha(150)
        s.fill((0, 0, 0))
        Utils.screen.blit(s, (0,0))

        # Dibujar el titulo de Arriba
        txtSuperior = Utils.dialogue_Font.render("Examinando item: ", True, 'white')
        Utils.screen.blit(txtSuperior, (20, 20))
        
        # Dibujar el titulo del objeto
        txtNombreObjeto = Utils.tittle_Font.render(self.nombre, True, "white")
        Utils.screen.blit(txtNombreObjeto, (ANCHO/2 - txtNombreObjeto.get_width()/2, 50))
        

        if self.tipo == "Nota":
            text_rect = self.texto.get_rect(center=(ANCHO/2, 100))
            Utils.screen.blit(self.texto, text_rect)

        if self.tipo == "Imagen":
            Utils.screen.blit(self.imagen, (ANCHO/2 - self.imagen.get_size()[0]/2, ALTO/2 - self.imagen.get_size()[1]/2))
            pass

        # Dibujar borde del boton inferior
        #rectBorde = pygame.rect.Rect(ANCHO/2-175, ALTO-50, 350, 100)
        #pygame.draw.rect(screen, 'gray', rectBorde, 0, 5)

        # Dibujar boton inferior
        self.btn_regresar.draw()

# Clase para manejar los cuartos
class Habitacion:
    def __init__(self, nombre, imagen, items: Item) -> None:
        self.nombre = nombre;
        self.imagen = imagen;
        self.items = items;
        pass

    def draw(self, enable = True):
        Utils.screen.fill(WHITE);
        for item in self.items:
            item.draw(enable)
        pass


# Definir los "game Objects" (objetos que aparecen en el juego)
def Imprimir_Pantalla(texto):
    if DEBUG: print("(En pantalla)" + texto)
    global hablando
    global text_actual
    text_actual = texto
    hablando = True


def Mover_habitacion(nombreHabitacion):
    global habitacion_actual # Es necesario que sea global para que acceda a la variable del juego
    cuartoObjetivo = habitacion_actual
    if DEBUG: print("Moviendo a la habitacion " + nombreHabitacion)

    # Buscar entre todas las habitaciones
    for cuarto in habitaciones:
        if cuarto.nombre == nombreHabitacion:
            cuartoObjetivo = cuarto # Guardar la habitacion a la cual se va mover

    if DEBUG and cuartoObjetivo == habitacion_actual: print("No se encontro una habitacion de nombre " + nombreHabitacion)

    habitacion_actual = cuartoObjetivo

def Examinar(x):
    # Logica para examinar un objeto en pantalla
    global inspeccionando
    global item_examinar
    global items_examinables

    if DEBUG: print("Examinando..." + str(x))
    
    # Generar un item examinable de error
    item_examinar = Item_Examinable("Error",
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
                    imagen = "Imagenes/object.png"
                    )


puerta_Estudio = Item("Puerta Estudio",
                      col_puntos= [ [ANCHO-200, ALTO-550], [ANCHO, ALTO-550], [ANCHO, ALTO], [ANCHO-200,ALTO] ],
                      accion = lambda x="Estudio": Mover_habitacion(x)
                      )

laptop = Item("Laptop",
              rect = [ ANCHO/2, ALTO/2, 120, 80],
              accion = lambda x="Esta es una laptop muy antigua y que deberia de irse a la basura": Imprimir_Pantalla(x)
              )

celular = Item("Celular",
               col_puntos = [[ANCHO/2-200-20, ALTO/2-200-20], [ANCHO/2-200+20, ALTO/2-200-20], [ANCHO/2-200+20, ALTO/2-200+20], [ANCHO/2-200-20, ALTO/2-200+20]],
               accion = lambda x="Un iphone": Imprimir_Pantalla(x))

puerta_SalaPrincipal = Item("Puerta Sala Principal",
                            rect = [200, 550, 200, 500,],
                            accion = lambda x="Sala Principal": Mover_habitacion(x)
                            )

notaPequena = Item("Notita",
                   rect = [ ANCHO/2 - 30, ALTO/2-100, 100, 100 ],
                   accion = lambda x="Nota rara": Examinar(x)
                   )


## * DEFINICION DE ITEMS EXAMINABLES *
items_examinables = [
    Item_Examinable("Nota rara",
                    tipo="Imagen",
                    texto="Estas mirando un objeto raro",
                    imagen="Imagenes/error404.png",
                    ),
]

## * DEFINICION DE HABITACIONES
habitaciones = [
    Habitacion("Sala Principal",
               "nada aun",
               [pintura_sala, puerta_Estudio, celular, notaPequena]
               ),

    Habitacion("Estudio",
               "Nada aun",
               [laptop, puerta_SalaPrincipal, notaPequena]
               ),

]

## * FIN DE MODIFICACIONES

# Variables de uso durante el juego
inventario = []  # Para almacenar objetos del inventario
habitacion_actual = habitaciones[0]  # Habitacion de inicio

inspeccionando = False
item_examinar = False # debe cambiarse a un item

hablando = False

text_actual = ""
text_counter = 0
text_speed = 2
text_finalizado = False
text_clicked = False

def dibujar_texto():
    global text_counter
    global text_speed
    global text_actual
    global text_finalizado
    global text_clicked
    global hablando

    fondo_texto = pygame.rect.Rect((0, ALTO-300), (ANCHO, 300))
    pygame.draw.rect( Utils.screen, 'black', fondo_texto )
    if text_counter < text_speed * len(text_actual):
        text_counter += 1
    elif ( text_counter >= text_speed * len(text_actual) ):
        text_finalizado = True
        # Resetear las variables

    snip = Utils.font.render(text_actual[0:text_counter // text_speed], True, 'white')
    Utils.screen.blit(snip, (0+10, ALTO-300+10))

    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    if fondo_texto.collidepoint(mouse_pos): # Verifica que el mouse este dentro del rango del objeto
        # Si se hace click antes de qe termine, que se adelante el final
        if left_click == 1 and text_clicked == False:
            text_clicked = True
            text_counter = text_speed * len(text_actual)
            # Si ya termino, que se cierre la ventana
            if text_finalizado:
                text_finalizado = False
                hablando = False
                text_counter = 0

        if left_click == 0:
            text_clicked = False


# Main funcion que ejecuta el juego
def main():
    global habitacion_actual
    global inspeccionando
    global item_examinar

    # Main game loop
    running = True
    while running:
        
        timer.tick(60)
        # Dibujar el cuarto actual
        # Si es que se esta analizando, el cuarto no deberia ser interactuable
        habitacion_actual.draw(enable = not (inspeccionando or hablando)  )

        if inspeccionando == True:
            # Se dibuja la interfaz del item examinandose
            item_examinar.draw()
            # Se actuliza valor de inspeccionando de acuerdo al item examinar actual
            inspeccionando = item_examinar.activo

        if hablando == True:
            # Logica para generar texto en pantalla
            dibujar_texto()

        # Manejar los eventos del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Actualizar el display del juego (???)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

