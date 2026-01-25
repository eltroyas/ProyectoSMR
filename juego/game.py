"""
Lógica principal del juego - Estado, turnos y combate
"""

import random
from cards import BASE_DECK, CardType
from enemies import ENEMIES

class GameState:
    """Mantiene el estado del juego"""
    
    def __init__(self):
        # Estado del jugador
        self.max_hp = 100
        self.player_hp = 100
        self.block = 0
        self.current_energy = 3
        self.max_energy = 3
        
        # Sistema de cartas
        self.deck = BASE_DECK.copy()
        random.shuffle(self.deck)  # Mezclar mazo al inicio
        self.hand = []
        self.discard_pile = []
        
        # Sistema de enemigos
        self.enemy_index = 0
        self.current_enemy = None
        self.defeated_enemies = []
        
        # Estado del juego
        self.game_over = False
        self.victory = False
        self.show_narrative = False
        self.narrative_text = ""
        self.waiting_for_enemy_attack = False
        
        # Inicializar
        self.start_new_battle()
        self.draw_hand()
    
    def start_new_battle(self):
        """Inicia una nueva batalla con el siguiente enemigo"""
        # Validación anti-crash: verificar índice válido
        if self.enemy_index < 0 or self.enemy_index >= len(ENEMIES):
            self.current_enemy = None
            return
        
        # Crear nueva instancia del enemigo para esta batalla
        enemy_template = ENEMIES[self.enemy_index]
        from enemies import Enemy
        self.current_enemy = Enemy(
            enemy_template.name,
            enemy_template.max_hp,
            enemy_template.attack_damage,
            enemy_template.ascii_art,
            enemy_template.victory_narrative
        )
    
    def draw_hand(self):
        """Roba 3 cartas para la mano"""
        # Validación anti-crash: asegurar que hay cartas disponibles
        if not self.deck and not self.discard_pile:
            return
        
        if len(self.deck) < 3:
            # Mezclar descarte de vuelta al mazo
            if self.discard_pile:
                self.deck.extend(self.discard_pile)
                self.discard_pile = []
                random.shuffle(self.deck)
        
        # Robar hasta 3 cartas (o las disponibles)
        cards_to_draw = min(3, len(self.deck))
        for _ in range(cards_to_draw):
            if self.deck:
                self.hand.append(self.deck.pop(0))
    
    def play_card(self, card_index):
        """Juega una carta de la mano"""
        # Validación anti-crash: verificar índice válido
        if card_index is None or card_index < 0 or card_index >= len(self.hand):
            return False
        
        if not self.hand:
            return False
        
        card = self.hand[card_index]
        
        if not card or not card.can_play(self.current_energy):
            return False
        
        # Ejecutar efecto con validación
        try:
            success = card.play(self)
        except Exception:
            success = False
        
        if success:
            self.current_energy = max(0, self.current_energy - card.cost)
            if card_index < len(self.hand):
                self.discard_pile.append(self.hand.pop(card_index))
            # Si la energía llega a 0, activar espera de ataque enemigo
            if self.current_energy <= 0:
                self.waiting_for_enemy_attack = True
            return True
        
        return False
    
    def end_turn(self):
        """Termina el turno del jugador"""
        if self.current_energy <= 0:
            self.waiting_for_enemy_attack = True
    
    def enemy_attack(self):
        """El enemigo ataca al jugador"""
        # Validación anti-crash: verificar condiciones
        if not self.current_enemy or not self.waiting_for_enemy_attack:
            return
        
        try:
            # Procesar veneno del enemigo
            if hasattr(self.current_enemy, 'poison') and self.current_enemy.poison > 0:
                self.current_enemy.process_poison()
            
            # Calcular daño con validación
            damage = self.current_enemy.attack() if hasattr(self.current_enemy, 'attack') else 0
            damage = max(0, damage)  # Asegurar que no sea negativo
            
            actual_damage = max(0, damage - self.block)
            self.block = max(0, self.block - damage)
            self.player_hp = max(0, self.player_hp - actual_damage)
            
            # Verificar derrota
            if self.player_hp <= 0:
                self.game_over = True
                return
            
            # Renovar mano y resetear energía
            self.current_energy = self.max_energy
            self.hand = []
            self.draw_hand()
            self.waiting_for_enemy_attack = False
        except Exception:
            # En caso de error, resetear estado de forma segura
            self.waiting_for_enemy_attack = False
            self.current_energy = self.max_energy
    
    def check_enemy_defeated(self):
        """Verifica si el enemigo actual está derrotado"""
        # Validación anti-crash: verificar que existe enemigo
        if not self.current_enemy:
            return
        
        try:
            if self.current_enemy.is_defeated():
                enemy_name = getattr(self.current_enemy, 'name', 'Enemigo Desconocido')
                self.defeated_enemies.append(enemy_name)
                self.show_narrative = True
                self.narrative_text = getattr(self.current_enemy, 'victory_narrative', '¡Enemigo derrotado!')
                self.enemy_index += 1
                
                # Validación: verificar si hay más enemigos
                if self.enemy_index >= len(ENEMIES):
                    self.victory = True
                    self.game_over = True
                else:
                    self.start_new_battle()
                    self.draw_hand()
                    self.current_energy = self.max_energy
        except Exception:
            # En caso de error, continuar sin crashear
            pass
    
    def update(self):
        """Actualiza el estado del juego"""
        if not self.game_over:
            self.check_enemy_defeated()
    
    def can_pass_turn(self):
        """Verifica si el jugador puede pasar el turno (no hay cartas jugables)"""
        if not self.hand:
            return True
        # Verificar si hay alguna carta jugable
        for card in self.hand:
            if card and card.can_play(self.current_energy):
                return False
        return True
    
    def pass_turn(self):
        """Pasa el turno manualmente cuando hay energía restante"""
        if self.current_energy > 0 and not self.waiting_for_enemy_attack:
            self.waiting_for_enemy_attack = True
            return True
        return False
    
    def handle_click(self, mouse_pos, ui):
        """Maneja los clics del mouse con validaciones anti-crash"""
        try:
            if self.game_over:
                if self.victory or self.player_hp <= 0:
                    # Verificar clic en botón de reintentar
                    if ui and ui.is_retry_button_clicked(mouse_pos):
                        self.__init__()  # Reiniciar juego
                return
            
            if self.show_narrative:
                # Clic para cerrar narrativa
                self.show_narrative = False
                return
            
            if self.waiting_for_enemy_attack:
                # Clic para que el enemigo ataque
                self.enemy_attack()
                return
            
            # Verificar clic en botón de pasar turno
            if ui and ui.is_pass_turn_button_clicked(mouse_pos, self):
                self.pass_turn()
                return
            
            # Verificar clic en cartas con validación
            if ui and self.hand:
                card_index = ui.get_clicked_card_index(mouse_pos, self.hand)
                if card_index is not None:
                    self.play_card(card_index)
                    return
        except Exception:
            # En caso de error, no crashear el juego
            pass

class Game:
    """Clase principal del juego"""
    
    def __init__(self):
        self.state = GameState()
    
    def update(self):
        """Actualiza el juego"""
        self.state.update()
    
    def handle_click(self, mouse_pos, ui):
        """Maneja clics"""
        self.state.handle_click(mouse_pos, ui)
