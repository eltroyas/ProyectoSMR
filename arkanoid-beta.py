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
BALL_VELOCIDAD_BASE = 6.5

BRICK_ANCHO = 68
BRICK_ALTO = 20
BRICK_PADDING = 8
BRICK_OFFSET_X = 36          # Ajustado para mejor centrado
BRICK_OFFSET_Y = 80

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE_ECO = (34, 139, 34)

NOMBRES_NIVEL = ["", "FÁCIL", "SENCILLO", "MEDIO"]

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Arkanoid - Ciudad Sostenible")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Arial", 26)
fuente_grande = pygame.font.SysFont("Arial", 48)

fondo_offset = 0

class Paleta:
    def __init__(self):
        self.rect = pygame.Rect(ANCHO//2 - PADDLE_ANCHO//2, PADDLE_Y, PADDLE_ANCHO, PADDLE_ALTO)

    def actualizar(self):
        keys = pygame.key.get_pressed()
        vel = 9
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= vel
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += vel
        if pygame.mouse.get_pressed()[0]:
            self.rect.centerx = pygame.mouse.get_pos()[0]

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(ANCHO, self.rect.right)

    def dibujar(self):
        pygame.draw.rect(pantalla, (100, 200, 100), self.rect)
        pygame.draw.rect(pantalla, BLANCO, self.rect, 4)


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
        pygame.draw.ellipse(pantalla, (200, 255, 200), self.rect, 2)


class Ladrillo:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_ANCHO, BRICK_ALTO)
        self.color = color

    def dibujar(self):
        pygame.draw.rect(pantalla, self.color, self.rect)
        pygame.draw.rect(pantalla, BLANCO, self.rect, 2)


# ==================== FONDO CIUDAD SOSTENIBLE ====================
def dibujar_fondo(offset):
    # Cielo
    for i in range(ALTO):
        color = (135 - i//6, 206 - i//8, 250 - i//10)
        pygame.draw.line(pantalla, color, (0, i), (ANCHO, i))

    # Edificios
    edificios = [(80, 420, 130), (230, 340, 95), (370, 460, 115), (510, 290, 135), (670, 390, 105)]
    for x, altura, ancho in edificios:
        px = (x + offset * 0.3) % (ANCHO + 150) - 70
        pygame.draw.rect(pantalla, (40, 90, 60), (px, ALTO - altura, ancho, altura))
        # Tejado solar
        pygame.draw.polygon(pantalla, (200, 200, 80), 
                           [(px, ALTO - altura), (px + ancho//2, ALTO - altura - 35), (px + ancho, ALTO - altura)])
        # Paneles solares
        for py in range(4):
            for px2 in range(3):
                pygame.draw.rect(pantalla, (220, 180, 60),
                                 (px + 15 + px2*27, ALTO - altura + 35 + py*38, 18, 22))

    # Árboles
    for ax in [90, 190, 460, 640, 740]:
        tx = (ax + offset * 0.7) % (ANCHO + 120) - 40
        pygame.draw.rect(pantalla, (34, 100, 34), (tx + 18, ALTO - 125, 18, 85))
        pygame.draw.circle(pantalla, VERDE_ECO, (tx + 27, ALTO - 145), 37)
        pygame.draw.circle(pantalla, VERDE_ECO, (tx + 10, ALTO - 170), 29)
        pygame.draw.circle(pantalla, VERDE_ECO, (tx + 45, ALTO - 165), 31)

    # Sol
    pygame.draw.circle(pantalla, (255, 235, 110), (680 + int(offset*0.08) % 180, 110), 48)


# ==================== CREAR LADRILLOS (mejor centrado) ====================
def crear_ladrillos(nivel):
    ladrillos = []
    colores = [(0, 255, 200), (0, 220, 100), (50, 255, 50), (180, 255, 80), (255, 240, 100), (255, 180, 60)]

    if nivel == 1:   # Muy fácil
        for fila in range(4):
            color = colores[fila]
            for col in range(8):
                x = BRICK_OFFSET_X + col * (BRICK_ANCHO + BRICK_PADDING)
                y = BRICK_OFFSET_Y + fila * (BRICK_ALTO + BRICK_PADDING)
                ladrillos.append(Ladrillo(x, y, color))

    elif nivel == 2:   # Sencillo
        for fila in range(5):
            color = colores[fila % 6]
            num_cols = 9 - fila
            start = (10 - num_cols) // 2
            for col in range(num_cols):
                x = BRICK_OFFSET_X + (start + col) * (BRICK_ANCHO + BRICK_PADDING)
                y = BRICK_OFFSET_Y + fila * (BRICK_ALTO + BRICK_PADDING)
                ladrillos.append(Ladrillo(x, y, color))

    elif nivel == 3:   # Medio
        for fila in range(6):
            color = colores[fila % 6]
            offset_x = 18 if fila % 2 == 1 else 0
            cols = 9 if fila % 2 == 1 else 10
            for col in range(cols):
                x = BRICK_OFFSET_X + col * (BRICK_ANCHO + BRICK_PADDING) + offset_x
                y = BRICK_OFFSET_Y + fila * (BRICK_ALTO + BRICK_PADDING)
                ladrillos.append(Ladrillo(x, y, color))

    return ladrillos


# ==================== VARIABLES ====================
paleta = Paleta()
bola = Bola()
current_level = 1
current_ball_speed = BALL_VELOCIDAD_BASE
ladrillos = crear_ladrillos(current_level)

puntos = 0
vidas = 3
estado = "esperando"
auto_launch = False
tiempo_reset = 0

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and estado == "esperando":
                vel = current_ball_speed
                bola.vel_x = random.choice([-vel, vel])
                bola.vel_y = -vel
                estado = "jugando"
                auto_launch = False

            if evento.key == pygame.K_r and estado in ["gameover", "ganado"]:
                puntos = 0
                vidas = 3
                current_level = 1
                current_ball_speed = BALL_VELOCIDAD_BASE
                ladrillos = crear_ladrillos(current_level)
                bola.reset(paleta)
                estado = "esperando"

    if estado == "jugando":
        paleta.actualizar()
        bola.actualizar()

        # === REBOTES MEJORADOS ===
        # Paredes laterales (con corrección anti-atascamiento)
        if bola.rect.left <= 0:
            bola.rect.left = 0
            bola.vel_x = abs(bola.vel_x) * 1.01   # pequeño impulso
        elif bola.rect.right >= ANCHO:
            bola.rect.right = ANCHO
            bola.vel_x = -abs(bola.vel_x) * 1.01

        if bola.rect.top <= 0:
            bola.rect.top = 0
            bola.vel_y = abs(bola.vel_y)

        # Caída
        if bola.rect.bottom >= ALTO:
            vidas -= 1
            if vidas > 0:
                bola.reset(paleta)
                estado = "esperando"
                auto_launch = True
                tiempo_reset = pygame.time.get_ticks()
            else:
                estado = "gameover"

        # Rebote en paleta (mejorado)
        if bola.rect.colliderect(paleta.rect) and bola.vel_y > 0:
            bola.vel_y *= -1
            golpe = (bola.rect.centerx - paleta.rect.left) / PADDLE_ANCHO
            bola.vel_x = current_ball_speed * (golpe - 0.5) * 2.9   # un poco más de control

        # Colisión con ladrillos
        for ladrillo in ladrillos[:]:
            if bola.rect.colliderect(ladrillo.rect):
                bola.vel_y *= -1
                ladrillos.remove(ladrillo)
                fila = int((ladrillo.rect.y - BRICK_OFFSET_Y) / (BRICK_ALTO + BRICK_PADDING))
                puntos += 10 * (7 - fila)
                break

        # Siguiente nivel
        if len(ladrillos) == 0:
            current_level += 1
            if current_level > 3:
                estado = "ganado"
            else:
                current_ball_speed = BALL_VELOCIDAD_BASE + (current_level - 1) * 1.3
                ladrillos = crear_ladrillos(current_level)
                bola.reset(paleta)
                estado = "esperando"
                auto_launch = True
                tiempo_reset = pygame.time.get_ticks()

    # Auto-lanzamiento
    if estado == "esperando" and auto_launch:
        if pygame.time.get_ticks() - tiempo_reset > 800:
            vel = current_ball_speed
            bola.vel_x = random.choice([-vel, vel])
            bola.vel_y = -vel
            estado = "jugando"
            auto_launch = False

    # ==================== DIBUJAR ====================
    dibujar_fondo(fondo_offset)
    fondo_offset += 0.45

    paleta.dibujar()
    bola.dibujar()
    for l in ladrillos:
        l.dibujar()

    # HUD
    pantalla.blit(fuente.render(f"PUNTOS: {puntos}", True, BLANCO), (20, 15))
    pantalla.blit(fuente.render(f"VIDAS: {vidas}", True, BLANCO), (ANCHO - 170, 15))
    pantalla.blit(fuente.render(f"NIVEL {current_level} - {NOMBRES_NIVEL[current_level]}", True, (255, 255, 120)), 
                  (ANCHO//2 - 135, 15))

    if estado == "esperando":
        bola.reset(paleta)
        msg = "PRESIONA ESPACIO PARA LANZAR" if not auto_launch else f"¡NIVEL {current_level} PREPARADO!"
        color = (100, 255, 150) if auto_launch else BLANCO
        txt = fuente.render(msg, True, color)
        pantalla.blit(txt, (ANCHO//2 - txt.get_width()//2, ALTO//2 - 30))

    elif estado == "gameover":
        pantalla.blit(fuente_grande.render("GAME OVER", True, (255, 80, 80)), (ANCHO//2 - 170, ALTO//2 - 60))
        pantalla.blit(fuente.render("Pulsa R para jugar otra vez", True, BLANCO), (ANCHO//2 - 180, ALTO//2 + 20))

    elif estado == "ganado":
        pantalla.blit(fuente_grande.render("¡SALVASTE LA CIUDAD SOSTENIBLE!", True, (100, 255, 150)), 
                      (ANCHO//2 - 285, ALTO//2 - 60))
        pantalla.blit(fuente.render("Pulsa R para jugar otra vez", True, BLANCO), (ANCHO//2 - 180, ALTO//2 + 20))

    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()
sys.exit()