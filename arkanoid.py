import pygame
import sys
import random

pygame.init()

# ==================== CONSTANTES ====================
ANCHO = 800
ALTO = 600
FPS = 60

PADDLE_ANCHO = 100
PADDLE_ALTO = 15
PADDLE_Y = ALTO - 50

BALL_RADIO = 10
BALL_VELOCIDAD_BASE = 7.5   # Velocidad inicial (nivel 1)

BRICK_ANCHO = 68
BRICK_ALTO = 20
BRICK_PADDING = 8
BRICK_OFFSET_X = 35
BRICK_OFFSET_Y = 60

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
COLORES_LADRILLOS = [
    (0, 255, 255),   # cian
    (0, 0, 255),     # azul
    (0, 255, 0),     # verde
    (255, 255, 0),   # amarillo
    (255, 165, 0),   # naranja
    (255, 0, 0)      # rojo
]

NOMBRES_NIVEL = ["", "FÁCIL", "MEDIO", "DIFÍCIL"]

# ==================== CONFIGURACIÓN DE PANTALLA ====================
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Arkanoid - 3 Niveles (Fácil / Medio / Difícil)")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Arial", 26)
fuente_grande = pygame.font.SysFont("Arial", 48)


class Paleta:
    def __init__(self):
        self.rect = pygame.Rect(ANCHO//2 - PADDLE_ANCHO//2, PADDLE_Y, PADDLE_ANCHO, PADDLE_ALTO)

    def actualizar(self):
        keys = pygame.key.get_pressed()
        velocidad = 9

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= velocidad
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += velocidad
        if pygame.mouse.get_pressed()[0]:          # Click izquierdo del ratón
            self.rect.centerx = pygame.mouse.get_pos()[0]

        # Limitar a los bordes
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO

    def dibujar(self):
        pygame.draw.rect(pantalla, BLANCO, self.rect)
        pygame.draw.rect(pantalla, (180, 180, 180), self.rect, 4)


class Bola:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, BALL_RADIO*2, BALL_RADIO*2)
        self.vel_x = 0
        self.vel_y = 0

    def reset(self, paleta):
        self.rect.centerx = paleta.rect.centerx
        self.rect.bottom = paleta.rect.top - 2
        self.vel_x = 0
        self.vel_y = 0

    def actualizar(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def dibujar(self):
        pygame.draw.ellipse(pantalla, BLANCO, self.rect)


class Ladrillo:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_ANCHO, BRICK_ALTO)
        self.color = color

    def dibujar(self):
        pygame.draw.rect(pantalla, self.color, self.rect)
        pygame.draw.rect(pantalla, BLANCO, self.rect, 2)


# ==================== CREACIÓN DE LADRILLOS SEGÚN NIVEL ====================
def crear_ladrillos(nivel):
    ladrillos = []

    if nivel == 1:        # Fácil - Bloque completo
        for fila in range(6):
            color = COLORES_LADRILLOS[fila]
            for col in range(10):
                x = BRICK_OFFSET_X + col * (BRICK_ANCHO + BRICK_PADDING)
                y = BRICK_OFFSET_Y + fila * (BRICK_ALTO + BRICK_PADDING)
                ladrillos.append(Ladrillo(x, y, color))

    elif nivel == 2:      # Medio - Pirámide centrada
        for fila in range(6):
            color = COLORES_LADRILLOS[fila]
            num_cols = 10 - fila
            start_col = (10 - num_cols) // 2
            for col in range(num_cols):
                x = BRICK_OFFSET_X + (start_col + col) * (BRICK_ANCHO + BRICK_PADDING)
                y = BRICK_OFFSET_Y + fila * (BRICK_ALTO + BRICK_PADDING)
                ladrillos.append(Ladrillo(x, y, color))

    elif nivel == 3:      # Difícil - Patrón escalonado (ladrillos desplazados)
        for fila in range(6):
            color = COLORES_LADRILLOS[fila]
            offset_x = 0 if fila % 2 == 0 else 38
            cols = 10 if fila % 2 == 0 else 9
            for col in range(cols):
                x = BRICK_OFFSET_X + col * (BRICK_ANCHO + BRICK_PADDING) + offset_x
                y = BRICK_OFFSET_Y + fila * (BRICK_ALTO + BRICK_PADDING)
                ladrillos.append(Ladrillo(x, y, color))

    return ladrillos


# ==================== VARIABLES DEL JUEGO ====================
paleta = Paleta()
bola = Bola()
current_level = 1
current_ball_speed = BALL_VELOCIDAD_BASE
ladrillos = crear_ladrillos(current_level)

puntos = 0
vidas = 3
estado = "esperando"      # esperando, jugando, gameover, ganado
auto_launch = False
tiempo_reset = 0

# ==================== BUCLE PRINCIPAL ====================
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:
            # Lanzar la bola
            if evento.key == pygame.K_SPACE and estado == "esperando":
                vel = current_ball_speed
                bola.vel_x = random.choice([-vel, vel])
                bola.vel_y = -vel
                estado = "jugando"
                auto_launch = False

            # Reiniciar con R (game over o victoria)
            if evento.key == pygame.K_r and estado in ["gameover", "ganado"]:
                puntos = 0
                vidas = 3
                current_level = 1
                current_ball_speed = BALL_VELOCIDAD_BASE
                ladrillos = crear_ladrillos(current_level)
                bola.reset(paleta)
                estado = "esperando"
                auto_launch = False

    # ====================== LÓGICA DEL JUEGO ======================
    if estado == "jugando":
        paleta.actualizar()
        bola.actualizar()

        # Rebotes en paredes
        if bola.rect.left <= 0 or bola.rect.right >= ANCHO:
            bola.vel_x *= -1
        if bola.rect.top <= 0:
            bola.vel_y *= -1

        # Caída de la bola
        if bola.rect.bottom >= ALTO:
            vidas -= 1
            if vidas > 0:
                bola.reset(paleta)
                estado = "esperando"
                auto_launch = True
                tiempo_reset = pygame.time.get_ticks()
            else:
                estado = "gameover"

        # Rebote en la paleta
        if bola.rect.colliderect(paleta.rect) and bola.vel_y > 0:
            bola.vel_y *= -1
            golpe = (bola.rect.centerx - paleta.rect.left) / PADDLE_ANCHO
            bola.vel_x = current_ball_speed * (golpe - 0.5) * 2.8

        # Colisión con ladrillos
        for ladrillo in ladrillos[:]:
            if bola.rect.colliderect(ladrillo.rect):
                bola.vel_y *= -1
                ladrillos.remove(ladrillo)
                fila = int((ladrillo.rect.y - BRICK_OFFSET_Y) / (BRICK_ALTO + BRICK_PADDING))
                puntos += 10 * (6 - fila)
                break

        # Pasar de nivel
        if len(ladrillos) == 0:
            current_level += 1
            if current_level > 3:
                estado = "ganado"
            else:
                current_ball_speed = BALL_VELOCIDAD_BASE + (current_level - 1) * 1.5
                ladrillos = crear_ladrillos(current_level)
                bola.reset(paleta)
                estado = "esperando"
                auto_launch = True
                tiempo_reset = pygame.time.get_ticks()

    # Auto-lanzamiento después de perder una vida o pasar nivel
    if estado == "esperando" and auto_launch:
        if pygame.time.get_ticks() - tiempo_reset > 800:   # 0.8 segundos
            vel = current_ball_speed
            bola.vel_x = random.choice([-vel, vel])
            bola.vel_y = -vel
            estado = "jugando"
            auto_launch = False

    # ====================== DIBUJAR ======================
    pantalla.fill(NEGRO)
    pygame.draw.rect(pantalla, BLANCO, (0, 0, ANCHO, ALTO), 8)

    paleta.dibujar()
    bola.dibujar()
    for ladrillo in ladrillos:
        ladrillo.dibujar()

    # HUD
    pantalla.blit(fuente.render(f"PUNTOS: {puntos}", True, BLANCO), (20, 15))
    pantalla.blit(fuente.render(f"VIDAS: {vidas}", True, BLANCO), (ANCHO - 170, 15))
    pantalla.blit(fuente.render(f"NIVEL {current_level} - {NOMBRES_NIVEL[current_level]}", 
                                True, (255, 215, 0)), (ANCHO//2 - 110, 15))

    # Mensajes según el estado
    if estado == "esperando":
        bola.reset(paleta)
        if auto_launch:
            txt = fuente.render(f"NIVEL {current_level} - {NOMBRES_NIVEL[current_level]} ¡Preparado!", 
                                True, (0, 255, 100))
        else:
            txt = fuente.render("PRESIONA ESPACIO PARA EMPEZAR", True, BLANCO)
        pantalla.blit(txt, (ANCHO//2 - txt.get_width()//2, ALTO//2 - 30))

    elif estado == "gameover":
        pantalla.blit(fuente_grande.render("GAME OVER", True, (255, 50, 50)), 
                      (ANCHO//2 - 160, ALTO//2 - 60))
        pantalla.blit(fuente.render("Pulsa R para jugar otra vez", True, BLANCO), 
                      (ANCHO//2 - 170, ALTO//2 + 20))

    elif estado == "ganado":
        pantalla.blit(fuente_grande.render("¡GANASTE EL JUEGO!", True, (0, 255, 100)), 
                      (ANCHO//2 - 220, ALTO//2 - 60))
        pantalla.blit(fuente.render("Pulsa R para jugar otra vez", True, BLANCO), 
                      (ANCHO//2 - 170, ALTO//2 + 20))

    pygame.display.flip()
    reloj.tick(FPS)


pygame.quit()
sys.exit()