from enum import Enum
from Item import Item
import pygame
import pygame_gui
import Utils

# Clase para definir los UNICOS tipos de items examinalbes
class Tipo_Examinable(Enum):
    Nota = 0
    Imagen = 1
    Puzzle = 2

#! Pueden existir (por ahora) solo tipos "Imagen", "Nota", "Puzzle"
class Examinable:
    def __init__(self, nombre, tipo: Tipo_Examinable, imagen = "error404.png", escalaImagen = 1.0, texto = "No haz asignado ningun texto",
                 accion_puzzle = None, puzzleAns = "None"):
        self.nombre = nombre
        self.tipo = tipo
        self.activo = True
        self.btn_regresar = Item("Regresar ...", col_rect= [Utils.ANCHO/2-200, Utils.ALTO-50, 400, 100], accion = self.cambiar_Activo, color=(40, 40, 40))
        
        if tipo == Tipo_Examinable.Imagen:
            # Logica para renderizar la imagen
            self.surface_imagen = Utils.get_imagen_cache(imagen)
            self.surface_imagen = pygame.transform.scale(self.surface_imagen, (self.surface_imagen.get_width() * escalaImagen, self.surface_imagen.get_height()*escalaImagen))
        
        elif tipo == Tipo_Examinable.Nota:
            self.surface_texto = Utils.tooltip_Font.render(texto, False, (250,250,250))
        
        elif tipo == Tipo_Examinable.Puzzle:
            # Generar la entrada de texto
            self.input_Texto = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((Utils.ANCHO/2 - 100, Utils.ALTO/2 - 50), (200, 100)), manager=Utils.Manager_Ui, object_id="#input_Puzzle")
            self.input_Texto.hide()

            # Generar Los botones de submit y limpiar
            self.btn_submit = Item("Submit", col_rect = [Utils.ANCHO/2 + 100, Utils.ALTO/2-50, 100, 100], accion = self.submit_puzzle, color=(255, 255, 255), tooltip="")
            self.btn_limpiar = Item("LimpiarInput", col_rect = [Utils.ANCHO/2 + 200, Utils.ALTO/2-50, 100, 100], accion = self.limpiar_input, color=(200, 200, 200), tooltip="")

            self.accion_puzzle = accion_puzzle
            self.puzzleAnswer = puzzleAns
    
    def submit_puzzle(self):
        if self.input_Texto.get_text() == self.puzzleAnswer:
            if Utils.DEBUG: print(self.nombre + "> LO RESOLVISTE EL PUZZLE")
        else:
            if Utils.DEBUG: print(self.nombre + "> Rpta equivocada el puzzle")

    def limpiar_input(self):
        if Utils.DEBUG: print(self.nombre + "> Limpiando texto")
        self.input_Texto.set_text("")

    # Funcion para la lambda
    def cambiar_Activo(self):
        if self.tipo == Tipo_Examinable.Puzzle:
            self.input_Texto.hide()
        self.activo = False

    def draw(self):
        self.activo = True #asumimos, por definicion, que si lo quisiste dibujar, es porque quieres activarlo

        # Dibujar capa negra transparente encima
        s = pygame.Surface((Utils.ANCHO, Utils.ALTO))
        s.set_alpha(150)
        s.fill((0, 0, 0))
        Utils.screen.blit(s, (0,0))

        # Dibujar el titulo de Arriba
        txtSuperior = Utils.dialogue_Font.render("Examinando item: ", True, 'white')
        Utils.screen.blit(txtSuperior, (20, 20))
        
        # Dibujar el titulo del objeto
        txtNombreObjeto = Utils.tittle_Font.render(self.nombre, True, "white")
        Utils.screen.blit(txtNombreObjeto, (Utils.ANCHO/2 - txtNombreObjeto.get_width()/2, 50))
        

        if self.tipo == Tipo_Examinable.Nota:
            text_rect = self.surface_texto.get_rect( center=(Utils.ANCHO/2, 100) )
            Utils.screen.blit( self.surface_texto, text_rect )


        if self.tipo == Tipo_Examinable.Imagen:
            Utils.screen.blit(self.surface_imagen, (Utils.ANCHO/2 - self.surface_imagen.get_size()[0]/2, Utils.ALTO/2 - self.surface_imagen.get_size()[1]/2))
            pass

        if self.tipo == Tipo_Examinable.Puzzle:
            self.btn_submit.draw()
            self.btn_limpiar.draw()
            self.input_Texto.show()

        # Dibujar borde del boton inferior
        #rectBorde = pygame.rect.Rect(ANCHO/2-175, ALTO-50, 350, 100)
        #pygame.draw.rect(screen, 'gray', rectBorde, 0, 5)

        # Dibujar boton inferior
        self.btn_regresar.draw()