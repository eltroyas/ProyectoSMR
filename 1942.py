### JUEGO PYTHON BASADO EN 1942 NES

import pygame      # Importamos la librería Pygame que nos permite crear ventanas, dibujar y detectar teclas
import sys         # Nos permite cerrar el programa correctamente cuando el usuario cierra la ventana
import random      # Nos permite generar números aleatorios (para la posición de los obstáculos)

# =============================================
# INICIALIZACIÓN DE PYGAME
# =============================================

pygame.init()      # Esta línea es obligatoria. Inicializa todos los módulos internos de Pygame 
                   # (ventana, sonido, teclado, etc.). Sin ella el juego no funciona.

# Definimos el tamaño de la ventana del juego
ANCHO = 800        # Ancho de la pantalla en píxeles
ALTO = 600         # Alto de la pantalla en píxeles

# Creamos la ventana donde se verá el juego
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dodger - Evita los obstáculos que caen")  # Título que aparece arriba de la ventana

# Definimos algunos colores en formato RGB (Rojo, Verde, Azul). Cada número va de 0 a 255.
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Creamos un reloj que controla la velocidad del juego (FPS)
reloj = pygame.time.Clock()

# =============================================
# VARIABLES DEL JUEGO (todas son variables normales, no clases)
# =============================================

# --- Jugador (el rectángulo verde que controlas) ---
player_x = ANCHO // 2 - 25      # Posición horizontal inicial (casi centrado). // es división entera
player_y = ALTO - 80            # Posición vertical (cerca de la parte inferior)
player_ancho = 50               # Ancho del jugador
player_alto = 50                # Alto del jugador
player_vel = 8                  # Velocidad de movimiento (cuántos píxeles se mueve por frame)

# --- Obstáculos (los rectángulos rojos que caen) ---
obstaculos = []                 # Lista vacía donde guardaremos todos los obstáculos.
                                # Cada obstáculo será una lista: [x, y, ancho, alto]

velocidad_obstaculos = 6        # Velocidad a la que caen los obstáculos
frecuencia_spawn = 25           # Cada cuántos frames aparece un nuevo obstáculo (aprox.)
frame_contador = 0              # Contador de frames para controlar cuándo spawnear obstáculos

# --- Otras variables del juego ---
puntuacion = 0                  # Puntos del jugador
vidas = 3                       # Vidas restantes
juego_activo = True             # Variable booleana (True/False) que indica si el juego sigue corriendo

# =============================================
# FUNCIÓN PARA DIBUJAR TODO EN PANTALLA
# =============================================

def dibujar():
    """Esta función se encarga de borrar y dibujar todo en cada frame"""
    pantalla.fill(NEGRO)                    # Borra toda la pantalla pintándola de negro
    
    # Dibujamos al jugador (un rectángulo verde)
    pygame.draw.rect(pantalla, VERDE, (player_x, player_y, player_ancho, player_alto))
    
    # Dibujamos todos los obstáculos que hay en la lista
    for obs in obstaculos:
        pygame.draw.rect(pantalla, ROJO, (obs[0], obs[1], obs[2], obs[3]))
    
    # Mostramos puntuación y vidas en la esquina superior
    fuente = pygame.font.SysFont(None, 36)   # Creamos una fuente de texto
    texto_puntos = fuente.render(f"Puntos: {puntuacion}", True, BLANCO)
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, BLANCO)
    
    pantalla.blit(texto_puntos, (10, 10))    # Dibujamos el texto en la pantalla
    pantalla.blit(texto_vidas, (ANCHO - 160, 10))
    
    # Si el juego terminó, mostramos mensaje de Game Over
    if not juego_activo:
        fuente_grande = pygame.font.SysFont(None, 60)
        texto_over = fuente_grande.render("GAME OVER", True, ROJO)
        texto_reiniciar = fuente.render("Presiona R para jugar de nuevo", True, BLANCO)
        pantalla.blit(texto_over, (ANCHO//2 - 160, ALTO//2 - 50))
        pantalla.blit(texto_reiniciar, (ANCHO//2 - 220, ALTO//2 + 20))
    
    pygame.display.flip()   # Actualiza la pantalla para que se vean los cambios

# =============================================
# BUCLE PRINCIPAL DEL JUEGO
# =============================================

while True:                     # Bucle infinito: el juego se actualiza constantemente
    
    frame_contador += 1         # Aumentamos el contador de frames en cada iteración
    
    # --- 1. Procesar eventos (teclado y cerrar ventana) ---
    for evento in pygame.event.get():           # Recorremos todos los eventos que ocurrieron
        if evento.type == pygame.QUIT:          # Si el usuario cierra la ventana
            pygame.quit()                       # Cerramos Pygame
            sys.exit()                          # Salimos del programa
        
        # Reiniciar el juego cuando termina
        if evento.type == pygame.KEYDOWN and not juego_activo:
            if evento.key == pygame.K_r:        # Si se presiona la tecla R
                # Reiniciamos todas las variables
                player_x = ANCHO // 2 - 25
                obstaculos.clear()              # Vaciamos la lista de obstáculos
                puntuacion = 0
                vidas = 3
                juego_activo = True
                frame_contador = 0
    
    if not juego_activo:                        # Si perdiste, solo dibujamos y esperamos
        dibujar()
        reloj.tick(60)
        continue
    
    # --- 2. Movimiento del jugador ---
    teclas = pygame.key.get_pressed()           # Obtenemos el estado actual de todas las teclas
    
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:     # Izquierda (flecha o tecla A)
        player_x -= player_vel
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:    # Derecha (flecha o tecla D)
        player_x += player_vel
    
    # Evitamos que el jugador salga de la pantalla por los lados
    if player_x < 0:
        player_x = 0
    if player_x > ANCHO - player_ancho:
        player_x = ANCHO - player_ancho
    
    # --- 3. Generar nuevos obstáculos ---
    if frame_contador % frecuencia_spawn == 0:          # Cada X frames aparece uno
        obs_ancho = random.randint(40, 90)              # Ancho aleatorio
        obs_x = random.randint(0, ANCHO - obs_ancho)    # Posición X aleatoria
        obstaculos.append([obs_x, -50, obs_ancho, 50]) # Añadimos el obstáculo a la lista
    
    # --- 4. Mover los obstáculos hacia abajo ---
    for obs in obstaculos[:]:           # Usamos [:] para poder eliminar mientras recorremos
        obs[1] += velocidad_obstaculos  # Bajamos la posición Y del obstáculo
        
        # Si el obstáculo ya pasó la pantalla, lo eliminamos y sumamos puntos
        if obs[1] > ALTO:
            obstaculos.remove(obs)
            puntuacion += 10
    
    # --- 5. Comprobar colisiones ---
    # Creamos un rectángulo invisible para el jugador (para detectar colisiones)
    player_rect = pygame.Rect(player_x, player_y, player_ancho, player_alto)
    
    for obs in obstaculos[:]:
        obs_rect = pygame.Rect(obs[0], obs[1], obs[2], obs[3])   # Rectángulo del obstáculo
        
        if player_rect.colliderect(obs_rect):       # Si hay colisión
            vidas -= 1                              # Perdemos una vida
            obstaculos.remove(obs)                  # Eliminamos ese obstáculo
            
            if vidas <= 0:                          # Si ya no quedan vidas
                juego_activo = False                # Terminamos el juego
    
    # --- 6. Dibujar todo y controlar velocidad ---
    dibujar()
    reloj.tick(60)          # Mantiene el juego a 60 fotogramas por segundo
