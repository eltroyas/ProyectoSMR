"""
Sistema de Cartas del Juego
Cartas temáticas de Biotecnología, Computación Cuántica y Exploración Espacial
"""

from enum import Enum

class CardType(Enum):
    BIOTECH = "Biotecnología"
    QUANTUM = "Cuántica"
    SPACE = "Espacial"

class Card:
    """Representa una carta del juego"""
    
    def __init__(self, name, cost, card_type, description, effect_func=None):
        self.name = name
        self.cost = cost
        self.card_type = card_type
        self.description = description
        self.effect_func = effect_func  # Función que ejecuta el efecto de la carta
    
    def play(self, game_state):
        """Ejecuta el efecto de la carta"""
        if self.effect_func:
            return self.effect_func(game_state)
        return False
    
    def can_play(self, energy):
        """Verifica si la carta puede ser jugada con la energía disponible"""
        return energy >= self.cost

# Efectos de cartas
def qbit_extra_effect(game_state):
    """Aumenta la energía en +1 para este turno"""
    game_state.current_energy += 1
    return True

def biotech_heal_effect(game_state):
    """Cura 5 HP al planeta"""
    game_state.player_hp = min(game_state.max_hp, game_state.player_hp + 5)
    return True

def quantum_attack_effect(game_state):
    """Inflige 8 de daño al enemigo actual"""
    if game_state.current_enemy:
        game_state.current_enemy.take_damage(8)
    return True

def space_shield_effect(game_state):
    """Otorga 3 de bloqueo"""
    game_state.block += 3
    return True

def biotech_poison_effect(game_state):
    """Aplica 3 de veneno al enemigo"""
    if game_state.current_enemy:
        game_state.current_enemy.apply_poison(3)
    return True

def quantum_entangle_effect(game_state):
    """Inflige 5 de daño y roba una carta"""
    if game_state.current_enemy:
        game_state.current_enemy.take_damage(5)
    # Robar carta se maneja en game_state
    return True

def space_energy_boost_effect(game_state):
    """Inflige 4 de daño y gana 1 energía"""
    if game_state.current_enemy:
        game_state.current_enemy.take_damage(4)
    game_state.current_energy += 1
    return True

def bioplastic_effect(game_state):
    """Cura 3 HP y bloquea 2"""
    game_state.player_hp = min(game_state.max_hp, game_state.player_hp + 3)
    game_state.block += 2
    return True

def quantum_algorithm_effect(game_state):
    """Inflige 12 de daño"""
    if game_state.current_enemy:
        game_state.current_enemy.take_damage(12)
    return True

def satellite_defender_effect(game_state):
    """Gana 5 de bloqueo"""
    game_state.block += 5
    return True

# Deck base de cartas
BASE_DECK = [
    Card("Q-Bit Extra", 0, CardType.QUANTUM, 
         "Gana +1 energía este turno", qbit_extra_effect),
    Card("Cura Biológica", 1, CardType.BIOTECH, 
         "Cura 5 HP al planeta", biotech_heal_effect),
    Card("Qubit Atacante", 2, CardType.QUANTUM, 
         "Inflige 8 de daño", quantum_attack_effect),
    Card("Escudo Espacial", 1, CardType.SPACE, 
         "Gana 3 de bloqueo", space_shield_effect),
    Card("Toxina Verde", 2, CardType.BIOTECH, 
         "Aplica 3 de veneno", biotech_poison_effect),
    Card("Entrelazamiento", 2, CardType.QUANTUM, 
         "5 de daño y roba carta", quantum_entangle_effect),
    Card("Impulso Estelar", 1, CardType.SPACE, 
         "4 de daño y +1 energía", space_energy_boost_effect),
    Card("Bioplástico", 1, CardType.BIOTECH, 
         "Cura 3 HP y bloquea 2", bioplastic_effect),
    Card("Algoritmo Cuántico", 3, CardType.QUANTUM, 
         "Inflige 12 de daño", quantum_algorithm_effect),
    Card("Satélite Defensor", 2, CardType.SPACE, 
         "Gana 5 de bloqueo", satellite_defender_effect),
]
