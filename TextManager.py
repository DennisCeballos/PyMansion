import pygame
import Utils


class TextoManager():
    def __init__(self):
        self.lista_texto = []
        self.text_actual = 0
        self.text_counter = 0
        self.text_speed = 2
        self.text_finalizado = False
        self.text_clicked = False

        alto_fondo = 300
        self.fondo_texto = pygame.rect.Rect((0,Utils.ALTO-alto_fondo), (Utils.ANCHO, alto_fondo))

        pass

    def draw(self):
        pygame.draw.rect( Utils.screen, 'black', self.fondo_texto )

        if self.text_counter < self.text_speed * len( self.lista_texto[self.text_actual] ):
            self.text_counter += 1
        elif ( self.text_counter >= self.text_speed * len( self.lista_texto[self.text_actual] ) ):
            self.text_finalizado = True
            # Resetear las variables

    
    def update(self):
        hablando = True
        snip = Utils.font.render( str(self.lista_texto[self.text_actual])[0:self.text_counter // self.text_speed], True, 'white')
        Utils.screen.blit(snip, (0+10, Utils.ALTO-300+10))

        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        if self.fondo_texto.collidepoint(mouse_pos): # Verifica que el mouse este dentro del rango del objeto
            # Si se hace click antes de qe termine, que se adelante el final
            if left_click == 1 and self.text_clicked == False:
                self.text_clicked = True
                self.text_counter = self.text_speed * len( self.lista_texto[self.text_actual] )
                # Si ya termino, que se cierre la ventana
                if self.text_finalizado:
                    self.text_finalizado = False
                    
                    # Si ya se recorrieron todos los elementos de la lista
                    if len(self.lista_texto) == self.text_actual+1:
                        # Salir de la animacion de texto
                        # , reiniciar las variables
                        self.text_counter = 0
                        self.text_actual = 0
                        self.lista_texto = []
                        hablando = False
                    else:
                        print(f"Se hace una suma de {self.text_actual}")
                        # Repetir el bucle con un nuevo texto
                        self.text_actual = self.text_actual + 1
                        self.text_counter = 0

            if left_click == 0:
                self.text_clicked = False

        return hablando

