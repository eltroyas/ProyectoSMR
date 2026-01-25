"""
Juego de Cartas Roguelike Educativo - Proyecto Intermodular
Biotecnología, Computación Cuántica y Exploración Espacial
Desarrollado con Pygame y Pygbag para web
"""

import asyncio
import pygame
from game import Game
from ui import UI

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colores Deep Tech
DEEP_BLACK = (5, 5, 10)
EMERALD_GREEN = (0, 255, 127)  # Biotecnología
NEON_CYAN = (0, 255, 255)      # Cuántica
VIOLET_PURPLE = (138, 43, 226)  # Espacio

async def main():
    """Bucle principal del juego compatible con Pygbag"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Crisis Planetaria: Tecnología al Rescate")
    clock = pygame.time.Clock()
    
    game = Game()
    ui = UI(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    running = True
    
    while running:
        # Compatibilidad con Pygbag - yield control
        await asyncio.sleep(0)
        
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic izquierdo
                    mouse_pos = pygame.mouse.get_pos()
                    game.handle_click(mouse_pos, ui)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Actualizar estado del juego
        game.update()
        
        # Renderizar
        screen.fill(DEEP_BLACK)
        ui.render(game)
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
