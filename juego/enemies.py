"""
Sistema de Enemigos - Mini-jefes representando crisis planetarias
"""

class Enemy:
    """Representa un enemigo en el juego"""
    
    def __init__(self, name, max_hp, attack_damage, ascii_art, victory_narrative):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_damage = attack_damage
        self.ascii_art = ascii_art
        self.victory_narrative = victory_narrative
        self.poison = 0  # Veneno acumulado
    
    def take_damage(self, amount):
        """Recibe daño"""
        self.hp = max(0, self.hp - amount)
    
    def apply_poison(self, amount):
        """Aplica veneno"""
        self.poison += amount
    
    def process_poison(self):
        """Procesa el veneno al inicio del turno del enemigo"""
        if self.poison > 0:
            self.take_damage(self.poison)
            self.poison = max(0, self.poison - 1)
    
    def is_defeated(self):
        """Verifica si el enemigo está derrotado"""
        return self.hp <= 0
    
    def attack(self):
        """Retorna el daño del ataque"""
        return self.attack_damage

# Definición de los 3 mini-jefes
ENEMY_1_ASCII = """
    ╔═══════════════════╗
    ║  RESIDUOS         ║
    ║   PLÁSTICOS       ║
    ║                   ║
    ║   ▓▓▓▓▓▓▓▓▓▓▓▓   ║
    ║   ▓▓▓▓▓▓▓▓▓▓▓▓   ║
    ║   ▓▓▓▓▓▓▓▓▓▓▓▓   ║
    ║   ▓▓▓▓▓▓▓▓▓▓▓▓   ║
    ╚═══════════════════╝
"""

ENEMY_2_ASCII = """
    ╔═══════════════════╗
    ║  LOBBY            ║
    ║  NEGACIONISTA     ║
    ║                   ║
    ║      💼          ║
    ║     /|\\          ║
    ║    / | \\         ║
    ║   ╱  |  ╲        ║
    ║  ╱   |   ╲       ║
    ╚═══════════════════╝
"""

ENEMY_3_ASCII = """
    ╔═══════════════════╗
    ║  CRISIS           ║
    ║  ENERGÉTICA       ║
    ║                   ║
    ║      ⚡          ║
    ║     ⚡⚡⚡        ║
    ║    ⚡⚡⚡⚡⚡      ║
    ║   ⚡⚡⚡⚡⚡⚡⚡    ║
    ╚═══════════════════╝
"""

ENEMY_1_NARRATIVE = """
¡Crisis Resuelta: Residuos Plásticos!

La biotecnología ha desarrollado enzimas modificadas
genéticamente que descomponen plásticos en componentes
biodegradables. Bacterias especializadas procesan millones
de toneladas de residuos, transformando la contaminación
en recursos reutilizables.

El planeta respira aliviado.
"""

ENEMY_2_NARRATIVE = """
¡Crisis Resuelta: Lobby Negacionista!

La computación cuántica ha procesado millones de datos
climáticos en segundos, generando modelos predictivos
irrefutables. Los algoritmos cuánticos han demostrado
científicamente la urgencia climática, silenciando
la desinformación con evidencia cuántica.

La verdad prevalece.
"""

ENEMY_3_NARRATIVE = """
¡Crisis Resuelta: Crisis Energética!

La exploración espacial ha desplegado satélites solares
en órbita que transmiten energía limpia a la Tierra.
Reactores de fusión desarrollados en estaciones espaciales
proveen energía ilimitada y sostenible.

La humanidad ha alcanzado la independencia energética.
"""

# Lista de enemigos progresivos
ENEMIES = [
    Enemy("Residuos Plásticos", 50, 8, ENEMY_1_ASCII, ENEMY_1_NARRATIVE),
    Enemy("Lobby Negacionista", 75, 12, ENEMY_2_ASCII, ENEMY_2_NARRATIVE),
    Enemy("Crisis Energética", 100, 15, ENEMY_3_ASCII, ENEMY_3_NARRATIVE),
]
