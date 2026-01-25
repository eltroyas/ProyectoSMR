import pygame
import asyncio
import random
import math

# Inicialización
pygame.init()
ANCHO, ALTO = 500, 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
f_bold = pygame.font.SysFont("Arial", 20, bold=True)
f_card = pygame.font.SysFont("Arial", 14)
f_info = pygame.font.SysFont("Arial", 16)

# Colores
BIO, QUANTUM, SPACE = (50, 255, 100), (0, 200, 255), (180, 100, 255)
FONDO, ROJO, CIAN = (10, 10, 20), (255, 50, 50), (0, 255, 200)

class Carta:
    def __init__(self, nombre, coste, tipo, valor, desc):
        self.nombre, self.coste, self.tipo, self.valor, self.desc = nombre, coste, tipo, valor, desc
        self.color = BIO if tipo == "BIO" else QUANTUM if tipo == "QUANTUM" else SPACE

class Enemigo:
    def __init__(self, nombre, hp, ataque, desc_derrota, arte):
        self.nombre, self.hp_max = nombre, hp
        self.hp_actual = hp
        self.ataque = ataque
        self.desc_derrota = desc_derrota
        self.arte = arte

class Juego:
    def __init__(self):
        self.hp_jugador = 60
        self.energia_max = 3
        self.energia = 3
        self.escudo = 0
        self.mazo = [
            Carta("Nanobots", 1, "BIO", 15, "Limpia 15 de daño"),
            Carta("Bio-Sintesis", 1, "BIO", 10, "Sana 10 HP"),
            Carta("Q-Bit Extra", 0, "QUANTUM", 1, "+1 Energia"),
            Carta("Pulso Cuantico", 2, "QUANTUM", 25, "Impacto critico 25"),
            Carta("Escudo Satelital", 1, "SPACE", 15, "Proteccion 15"),
            Carta("Sonda Espacial", 1, "SPACE", 8, "Impacto 8 y Escudo 5")
        ]
        self.pool_enemigos = [
            Enemigo("RESIDUOS PLASTICOS", 50, 12, "La biotecnologia ha degradado el plastico oceánico.", [" ~~~ ","(ooo)"," ~~~ "]),
            Enemigo("LOBBY NEGACIONISTA", 70, 18, "La transparencia de datos cuanticos vencio al lobby.", ["  O  "," /|\\ "," / \\ "]),
            Enemigo("CRISIS ENERGETICA", 90, 22, "Red de fusion establecida. El futuro es brillante.", [" [!] "," /|\\ "," / \\ "])
        ]
        self.idx_enemigo = 0
        self.estado = "JUGANDO"
        self.log_texto = ""
        self.mano = []
        self.robar_mano()

    def robar_mano(self):
        self.mano = random.sample(self.mazo, 3)
        self.energia = self.energia_max

    def jugar_carta(self, idx):
        if idx >= len(self.mano): return
        c = self.mano[idx]
        if self.energia >= c.coste:
            self.energia -= c.coste
            if c.nombre == "Q-Bit Extra": self.energia += 1
            elif c.tipo == "BIO":
                if "Sana" in c.desc: self.hp_jugador = min(60, self.hp_jugador + c.valor)
                else: self.pool_enemigos[self.idx_enemigo].hp_actual -= c.valor
            elif c.tipo == "QUANTUM": self.pool_enemigos[self.idx_enemigo].hp_actual -= c.valor
            elif c.tipo == "SPACE":
                self.escudo += c.valor
                if "Sonda" in c.nombre: self.pool_enemigos[self.idx_enemigo].hp_actual -= 8
            self.mano.pop(idx)
            
            if self.pool_enemigos[self.idx_enemigo].hp_actual <= 0:
                self.log_texto = self.pool_enemigos[self.idx_enemigo].desc_derrota
                self.estado = "INFO_ENEMIGO"

    def turno_enemigo(self):
        daño = max(0, self.pool_enemigos[self.idx_enemigo].ataque - self.escudo)
        self.hp_jugador -= daño
        self.escudo = 0
        if self.hp_jugador <= 0: self.estado = "MUERTE"
        else: self.robar_mano()

async def main():
    j = Juego()
    while True:
        pantalla.fill(FONDO)
        
        # 1. Dibujar UI Superior
        pygame.draw.rect(pantalla, (30,30,50), (50, 30, 150, 15))
        pygame.draw.rect(pantalla, CIAN, (50, 30, (max(0,j.hp_jugador)/60)*150, 15))
        pantalla.blit(f_bold.render(f"PLANETA: {max(0,j.hp_jugador)} HP", True, (255,255,255)), (50, 5))

        if j.estado != "VICTORIA" and j.idx_enemigo < len(j.pool_enemigos):
            e = j.pool_enemigos[j.idx_enemigo]
            for i, l in enumerate(e.arte):
                pantalla.blit(f_bold.render(l, True, ROJO), (220, 100 + i*20))
            pantalla.blit(f_bold.render(e.nombre, True, ROJO), (150, 180))
            pygame.draw.rect(pantalla, ROJO, (150, 210, (max(0,e.hp_actual)/e.hp_max)*200, 10))

        # 2. Lógica de Estados
        if j.estado == "INFO_ENEMIGO":
            pygame.draw.rect(pantalla, (20,40,60), (50, 300, 400, 150), border_radius=10)
            y_p = 320
            for l in [j.log_texto]: # Texto de derrota
                pantalla.blit(f_info.render(l, True, (255,255,255)), (70, y_p))
            pantalla.blit(f_bold.render("[ CLIC PARA CONTINUAR ]", True, CIAN), (130, 410))

        elif j.estado == "MUERTE":
            pantalla.blit(f_bold.render("EL FUTURO HA SIDO CANCELADO", True, ROJO), (100, ALTO//2))
            pantalla.blit(f_info.render("Clic para reintentar", True, (200,200,200)), (180, ALTO//2 + 40))

        elif j.estado == "VICTORIA":
            pantalla.blit(f_bold.render("SISTEMA ESTABLE: FUTURO SALVADO", True, CIAN), (80, ALTO//2))

        elif j.estado == "JUGANDO":
            pantalla.blit(f_bold.render(f"ENERGIA: {j.energia}/3", True, QUANTUM), (50, 420))
            if j.escudo > 0: pantalla.blit(f_bold.render(f"ESCUDO: {j.escudo}", True, SPACE), (300, 420))
            for i, c in enumerate(j.mano):
                r = pygame.Rect(30 + i*155, 460, 140, 180)
                pygame.draw.rect(pantalla, (20,25,35), r, border_radius=10)
                pygame.draw.rect(pantalla, c.color, r, 2, border_radius=10)
                pantalla.blit(f_bold.render(c.nombre, True, (255,255,255)), (r.x+10, r.y+10))
                pantalla.blit(f_card.render(c.desc, True, (150,150,150)), (r.x+10, r.y+70))
            if j.energia == 0:
                pantalla.blit(f_bold.render("SIN ENERGIA - CLIC PARA TURNO ENEMIGO", True, ROJO), (60, 650))

        # 3. Eventos
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                x, y = ev.pos
                if j.estado == "INFO_ENEMIGO":
                    if j.idx_enemigo < len(j.pool_enemigos) - 1:
                        j.idx_enemigo += 1
                        j.estado = "JUGANDO"; j.robar_mano()
                    else: j.estado = "VICTORIA"
                elif j.estado == "MUERTE":
                    j = Juego()
                elif j.estado == "JUGANDO":
                    if j.energia > 0:
                        for i in range(len(j.mano)):
                            if (30 + i*155) < x < (30 + i*155 + 140) and 460 < y < 640:
                                j.jugar_carta(i); break
                    else: j.turno_enemigo()

        pygame.display.flip()
        await asyncio.sleep(0)
        reloj.tick(30)

asyncio.run(main())