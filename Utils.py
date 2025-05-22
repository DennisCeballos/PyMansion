import pygame
import pygame_gui

DEBUG = False

ANCHO = 810
ALTO = 810

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definicion de ciertos tipos de font por defecto
font          = pygame.font.Font(None, 36)
tooltip_Font  = pygame.font.Font(None, 26)
dialogue_Font = pygame.font.Font(None, 30)
tittle_Font   = pygame.font.Font(None, 35)

# Definicion de tamano de pantalla de juego por defecto
screen: pygame.Surface = pygame.display.set_mode((500,500))
# Definicion de tamano de pantalla para interactuar con la pantalla por defecto
Manager_Ui : pygame_gui.UIManager = pygame_gui.UIManager((500,500))

# Cargar imagenes
cache_imagenes = {}
cache_imagenes["default"] = pygame.image.load("./Imagenes/error404.png")

# Recibe la direccion de la imagen
def get_imagen_cache(nombre_imagen: str) -> pygame.Surface:
    if not nombre_imagen in cache_imagenes:
        try:
            cache_imagenes[nombre_imagen] = pygame.image.load("./Imagenes/" + nombre_imagen).convert_alpha()
        except Exception:
            print("!!ERROR: no hay un archivo de imagen con el nombre " + nombre_imagen)
            return cache_imagenes["default"]

    return cache_imagenes[nombre_imagen]