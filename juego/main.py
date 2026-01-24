import pygame
import sys
import random
import asyncio # <--- 1. Importante: Necesario para la web

# Inicializar Pygame
pygame.init()

# Constantes
ANCHO = 400
ALTO = 600
FPS = 60

# Colores (se mantienen igual)
BLANCO = (255, 255, 255)
AZUL_CIELO = (135, 206, 235)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
MARRON = (139, 69, 19)

# Configuración de pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Flappy Bird - Web Version")
reloj = pygame.time.Clock()
fuente = pygame.font.Font(None, 36)
fuente_grande = pygame.font.Font(None, 72)

# Variables globales (se mantienen igual)
pajaro_x = 80
pajaro_y = ALTO // 2
velocidad_y = 0
gravedad = 0.5
salto = -10
radio_pajaro = 15
tubos = []
ancho_tubo = 70
hueco_tubo = 180
velocidad_tubos = 4
puntuacion = 0
juego_activo = True
suelo_x = 0

def reiniciar_juego():
    global pajaro_y, velocidad_y, tubos, puntuacion, juego_activo, suelo_x
    pajaro_y = ALTO // 2
    velocidad_y = 0
    tubos = []
    puntuacion = 0
    juego_activo = True
    suelo_x = 0

# 2. Definimos una función asíncrona principal
async def main():
    global pajaro_y, velocidad_y, tubos, puntuacion, juego_activo, suelo_x, ejecutando

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if juego_activo:
                        velocidad_y = salto
                    else:
                        reiniciar_juego()

        if juego_activo:
            velocidad_y += gravedad
            pajaro_y += velocidad_y

            if len(tubos) == 0 or tubos[-1]['x'] < ANCHO - 250:
                pos_hueco = random.randint(150, ALTO - 250)
                tubos.append({'x': ANCHO, 'hueco_y': pos_hueco, 'puntuado': False})

            for tubo in tubos:
                tubo['x'] -= velocidad_tubos

            tubos = [t for t in tubos if t['x'] > -ancho_tubo]

            for tubo in tubos:
                if tubo['x'] + ancho_tubo < pajaro_x and not tubo['puntuado']:
                    puntuacion += 1
                    tubo['puntuado'] = True

            pajaro_rect = pygame.Rect(pajaro_x - radio_pajaro, pajaro_y - radio_pajaro, radio_pajaro * 2, radio_pajaro * 2)
            if pajaro_y + radio_pajaro > ALTO - 100 or pajaro_y - radio_pajaro < 0:
                juego_activo = False

            for tubo in tubos:
                tubo_superior = pygame.Rect(tubo['x'], 0, ancho_tubo, tubo['hueco_y'] - hueco_tubo // 2)
                tubo_inferior = pygame.Rect(tubo['x'], tubo['hueco_y'] + hueco_tubo // 2, ancho_tubo, ALTO - 100 - (tubo['hueco_y'] + hueco_tubo // 2))
                if pajaro_rect.colliderect(tubo_superior) or pajaro_rect.colliderect(tubo_inferior):
                    juego_activo = False

        suelo_x -= velocidad_tubos
        if suelo_x <= -ANCHO:
            suelo_x = 0

        pantalla.fill(AZUL_CIELO)

        for tubo in tubos:
            pygame.draw.rect(pantalla, VERDE, (tubo['x'], 0, ancho_tubo, tubo['hueco_y'] - hueco_tubo // 2))
            pygame.draw.rect(pantalla, (0, 200, 0), (tubo['x'] - 10, tubo['hueco_y'] - hueco_tubo // 2 - 30, ancho_tubo + 20, 30))
            pygame.draw.rect(pantalla, VERDE, (tubo['x'], tubo['hueco_y'] + hueco_tubo // 2, ancho_tubo, ALTO - 100 - (tubo['hueco_y'] + hueco_tubo // 2)))
            pygame.draw.rect(pantalla, (0, 200, 0), (tubo['x'] - 10, tubo['hueco_y'] + hueco_tubo // 2, ancho_tubo + 20, 30))

        pygame.draw.circle(pantalla, AMARILLO, (int(pajaro_x), int(pajaro_y)), radio_pajaro)
        pygame.draw.circle(pantalla, NEGRO, (int(pajaro_x), int(pajaro_y)), radio_pajaro, 2)
        pygame.draw.circle(pantalla, BLANCO, (int(pajaro_x + 8), int(pajaro_y - 5)), 5)
        pygame.draw.circle(pantalla, NEGRO, (int(pajaro_x + 10), int(pajaro_y - 5)), 2)

        pygame.draw.rect(pantalla, MARRON, (suelo_x, ALTO - 100, ANCHO, 100))
        pygame.draw.rect(pantalla, GRIS, (suelo_x, ALTO - 100, ANCHO, 20))
        pygame.draw.rect(pantalla, MARRON, (suelo_x + ANCHO, ALTO - 100, ANCHO, 100))
        pygame.draw.rect(pantalla, GRIS, (suelo_x + ANCHO, ALTO - 100, ANCHO, 20))

        texto_puntuacion = fuente.render(f"Puntuacion: {puntuacion}", True, NEGRO)
        pantalla.blit(texto_puntuacion, (10, 10))

        if not juego_activo:
            texto_gameover = fuente_grande.render("GAME OVER", True, NEGRO)
            texto_rect = texto_gameover.get_rect(center=(ANCHO//2, ALTO//2 - 50))
            pantalla.blit(texto_gameover, texto_rect)
            texto_espacio = fuente.render("Presiona ESPACIO", True, NEGRO)
            texto_rect2 = texto_espacio.get_rect(center=(ANCHO//2, ALTO//2 + 20))
            pantalla.blit(texto_espacio, texto_rect2)

        pygame.display.flip()
        
        # 3. MUY IMPORTANTE PARA WEB:
        await asyncio.sleep(0) 
        reloj.tick(FPS)

# 4. Ejecutar la función principal
asyncio.run(main())