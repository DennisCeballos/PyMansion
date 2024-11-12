import pygame
import pygame_gui

DEBUG = True

ANCHO = 810
ALTO = 810

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font: pygame.font.Font = None
tooltip_Font: pygame.font.Font = None
dialogue_Font: pygame.font.Font = None
tittle_Font: pygame.font.Font = None

screen: pygame.Surface = None
Manager_Ui : pygame_gui.UIManager = None

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