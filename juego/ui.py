"""
Interfaz de Usuario - Renderizado con paleta Deep Tech
"""

import pygame
from cards import CardType

# Colores Deep Tech
DEEP_BLACK = (5, 5, 10)
EMERALD_GREEN = (0, 255, 127)  # Biotecnología
NEON_CYAN = (0, 255, 255)      # Cuántica
VIOLET_PURPLE = (138, 43, 226)  # Espacio
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Dimensiones
CARD_WIDTH = 200
CARD_HEIGHT = 280
CARD_SPACING = 20
CARD_START_Y = 400

class UI:
    """Maneja el renderizado de la interfaz"""
    
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)
        
        # Botón de reintentar
        self.retry_button_rect = pygame.Rect(width // 2 - 100, height // 2 + 50, 200, 50)
        
        # Botón de pasar turno (centro inferior)
        self.pass_turn_button_rect = pygame.Rect(width // 2 - 100, height - 80, 200, 50)
    
    def get_card_color(self, card_type):
        """Obtiene el color según el tipo de carta"""
        if card_type == CardType.BIOTECH:
            return EMERALD_GREEN
        elif card_type == CardType.QUANTUM:
            return NEON_CYAN
        elif card_type == CardType.SPACE:
            return VIOLET_PURPLE
        return GRAY
    
    def render_card(self, card, x, y, is_playable=True):
        """Renderiza una carta"""
        # Color de borde según tipo
        color = self.get_card_color(card.card_type)
        
        # Fondo de la carta
        card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(self.screen, DEEP_BLACK, card_rect)
        pygame.draw.rect(self.screen, color if is_playable else GRAY, card_rect, 3)
        
        # Nombre
        name_surface = self.font_medium.render(card.name, True, color if is_playable else GRAY)
        self.screen.blit(name_surface, (x + 10, y + 10))
        
        # Coste
        cost_surface = self.font_large.render(str(card.cost), True, YELLOW if is_playable else GRAY)
        cost_rect = cost_surface.get_rect(center=(x + CARD_WIDTH - 30, y + 30))
        self.screen.blit(cost_surface, cost_rect)
        
        # Tipo
        type_surface = self.font_tiny.render(card.card_type.value, True, color if is_playable else GRAY)
        self.screen.blit(type_surface, (x + 10, y + 50))
        
        # Descripción (con salto de línea)
        words = card.description.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font_tiny.size(test_line)[0] < CARD_WIDTH - 20:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        
        desc_y = y + 80
        for line in lines[:4]:  # Máximo 4 líneas
            desc_surface = self.font_tiny.render(line, True, WHITE)
            self.screen.blit(desc_surface, (x + 10, desc_y))
            desc_y += 20
    
    def get_clicked_card_index(self, mouse_pos, hand):
        """Retorna el índice de la carta clickeada, o None"""
        # Validación anti-crash
        if not hand or not mouse_pos:
            return None
        
        try:
            start_x = (self.width - (len(hand) * (CARD_WIDTH + CARD_SPACING) - CARD_SPACING)) // 2
            
            for i, card in enumerate(hand):
                if card:  # Validar que la carta existe
                    card_x = start_x + i * (CARD_WIDTH + CARD_SPACING)
                    card_rect = pygame.Rect(card_x, CARD_START_Y, CARD_WIDTH, CARD_HEIGHT)
                    if card_rect.collidepoint(mouse_pos):
                        return i
        except Exception:
            pass
        return None
    
    def render_enemy(self, enemy, game_state):
        """Renderiza el enemigo"""
        if not enemy:
            return
        
        try:
            # Panel del enemigo (lado izquierdo)
            enemy_panel = pygame.Rect(50, 50, 300, 300)
            pygame.draw.rect(self.screen, DEEP_BLACK, enemy_panel)
            pygame.draw.rect(self.screen, RED, enemy_panel, 3)
            
            # Nombre del enemigo
            enemy_name = getattr(enemy, 'name', 'Enemigo')
            name_surface = self.font_medium.render(enemy_name, True, RED)
            self.screen.blit(name_surface, (60, 60))
            
            # HP del enemigo con validación
            enemy_hp = max(0, getattr(enemy, 'hp', 0))
            enemy_max_hp = max(1, getattr(enemy, 'max_hp', 1))
            hp_text = f"HP: {enemy_hp}/{enemy_max_hp}"
            hp_surface = self.font_small.render(hp_text, True, WHITE)
            self.screen.blit(hp_surface, (60, 100))
            
            # Barra de HP
            hp_bar_width = 280
            hp_bar_height = 20
            hp_percent = min(1.0, max(0.0, enemy_hp / enemy_max_hp))
            hp_bar_rect = pygame.Rect(60, 130, hp_bar_width, hp_bar_height)
            pygame.draw.rect(self.screen, (50, 50, 50), hp_bar_rect)
            pygame.draw.rect(self.screen, RED, (60, 130, int(hp_bar_width * hp_percent), hp_bar_height))
            pygame.draw.rect(self.screen, WHITE, hp_bar_rect, 2)
            
            # Arte ASCII (simplificado - solo texto)
            ascii_art = getattr(enemy, 'ascii_art', '')
            if ascii_art:
                ascii_lines = ascii_art.strip().split('\n')
                ascii_y = 160
                for line in ascii_lines[:10]:  # Máximo 10 líneas
                    ascii_surface = self.font_tiny.render(line, True, RED)
                    self.screen.blit(ascii_surface, (60, ascii_y))
                    ascii_y += 15
        except Exception:
            pass  # No crashear si hay error al renderizar
    
    def render_player_info(self, game_state):
        """Renderiza la información del jugador"""
        # Panel del jugador (lado derecho)
        player_panel = pygame.Rect(self.width - 350, 50, 300, 200)
        pygame.draw.rect(self.screen, DEEP_BLACK, player_panel)
        pygame.draw.rect(self.screen, EMERALD_GREEN, player_panel, 3)
        
        # Título
        title_surface = self.font_medium.render("PLANETA", True, EMERALD_GREEN)
        self.screen.blit(title_surface, (self.width - 340, 60))
        
        # HP del jugador
        hp_text = f"HP: {game_state.player_hp}/{game_state.max_hp}"
        hp_surface = self.font_small.render(hp_text, True, WHITE)
        self.screen.blit(hp_surface, (self.width - 340, 100))
        
        # Barra de HP
        hp_bar_width = 280
        hp_bar_height = 20
        hp_percent = game_state.player_hp / game_state.max_hp
        hp_bar_rect = pygame.Rect(self.width - 340, 130, hp_bar_width, hp_bar_height)
        pygame.draw.rect(self.screen, (50, 50, 50), hp_bar_rect)
        color = EMERALD_GREEN if hp_percent > 0.3 else RED
        pygame.draw.rect(self.screen, color, (self.width - 340, 130, int(hp_bar_width * hp_percent), hp_bar_height))
        pygame.draw.rect(self.screen, WHITE, hp_bar_rect, 2)
        
        # Energía
        energy_text = f"Energía: {game_state.current_energy}/{game_state.max_energy}"
        energy_surface = self.font_small.render(energy_text, True, YELLOW)
        self.screen.blit(energy_surface, (self.width - 340, 160))
        
        # Bloqueo
        if game_state.block > 0:
            block_text = f"Bloqueo: {game_state.block}"
            block_surface = self.font_small.render(block_text, True, NEON_CYAN)
            self.screen.blit(block_surface, (self.width - 340, 190))
    
    def render_hand(self, hand, game_state):
        """Renderiza la mano de cartas"""
        if not hand:
            return
        
        try:
            start_x = (self.width - (len(hand) * (CARD_WIDTH + CARD_SPACING) - CARD_SPACING)) // 2
            
            for i, card in enumerate(hand):
                if card:  # Validar que la carta existe
                    card_x = start_x + i * (CARD_WIDTH + CARD_SPACING)
                    is_playable = card.can_play(game_state.current_energy) if hasattr(card, 'can_play') else False
                    self.render_card(card, card_x, CARD_START_Y, is_playable)
        except Exception:
            pass  # No crashear si hay error al renderizar
    
    def render_narrative(self, narrative_text):
        """Renderiza el cuadro narrativo"""
        # Fondo semi-transparente
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill(DEEP_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Cuadro de texto
        box_width = self.width - 200
        box_height = 400
        box_x = 100
        box_y = (self.height - box_height) // 2
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        
        pygame.draw.rect(self.screen, DEEP_BLACK, box_rect)
        pygame.draw.rect(self.screen, VIOLET_PURPLE, box_rect, 5)
        
        # Texto narrativo (con salto de línea)
        lines = narrative_text.strip().split('\n')
        text_y = box_y + 30
        for line in lines:
            if line.strip():
                text_surface = self.font_small.render(line, True, WHITE)
                self.screen.blit(text_surface, (box_x + 20, text_y))
            text_y += 30
        
        # Instrucción
        instruction = "Clic para continuar..."
        inst_surface = self.font_tiny.render(instruction, True, GRAY)
        inst_rect = inst_surface.get_rect(center=(self.width // 2, box_y + box_height - 30))
        self.screen.blit(inst_surface, inst_rect)
    
    def render_game_over(self, victory):
        """Renderiza la pantalla de fin de juego"""
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill(DEEP_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Mensaje
        if victory:
            message = "¡VICTORIA GLOBAL!"
            color = EMERALD_GREEN
            submessage = "La humanidad ha superado todas las crisis"
        else:
            message = "DERROTA"
            color = RED
            submessage = "El planeta ha sucumbido a las crisis"
        
        msg_surface = self.font_large.render(message, True, color)
        msg_rect = msg_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.screen.blit(msg_surface, msg_rect)
        
        sub_surface = self.font_medium.render(submessage, True, WHITE)
        sub_rect = sub_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(sub_surface, sub_rect)
        
        # Botón de reintentar
        pygame.draw.rect(self.screen, NEON_CYAN, self.retry_button_rect)
        pygame.draw.rect(self.screen, WHITE, self.retry_button_rect, 2)
        retry_text = self.font_medium.render("Reintentar", True, DEEP_BLACK)
        retry_rect = retry_text.get_rect(center=self.retry_button_rect.center)
        self.screen.blit(retry_text, retry_rect)
    
    def is_retry_button_clicked(self, mouse_pos):
        """Verifica si se clickeó el botón de reintentar"""
        return self.retry_button_rect.collidepoint(mouse_pos)
    
    def render_waiting_message(self):
        """Renderiza mensaje cuando se espera el ataque del enemigo"""
        message = "Clic para que el enemigo ataque"
        msg_surface = self.font_medium.render(message, True, YELLOW)
        msg_rect = msg_surface.get_rect(center=(self.width // 2, 350))
        self.screen.blit(msg_surface, msg_rect)
    
    def render_pass_turn_button(self, game_state):
        """Renderiza el botón de pasar turno si es posible"""
        # Solo mostrar si hay energía y no hay cartas jugables
        if game_state.current_energy > 0 and game_state.can_pass_turn():
            # Dibujar botón
            pygame.draw.rect(self.screen, NEON_CYAN, self.pass_turn_button_rect)
            pygame.draw.rect(self.screen, WHITE, self.pass_turn_button_rect, 2)
            
            # Texto del botón
            pass_text = self.font_medium.render("Pasar Turno", True, DEEP_BLACK)
            pass_rect = pass_text.get_rect(center=self.pass_turn_button_rect.center)
            self.screen.blit(pass_text, pass_rect)
    
    def is_pass_turn_button_clicked(self, mouse_pos, game_state):
        """Verifica si se clickeó el botón de pasar turno"""
        if game_state.current_energy > 0 and game_state.can_pass_turn():
            return self.pass_turn_button_rect.collidepoint(mouse_pos)
        return False
    
    def render(self, game):
        """Renderiza todo el juego"""
        game_state = game.state
        
        # Renderizar información del jugador
        self.render_player_info(game_state)
        
        # Renderizar enemigo
        if game_state.current_enemy:
            self.render_enemy(game_state.current_enemy, game_state)
        
        # Renderizar mano de cartas
        if not game_state.game_over and not game_state.show_narrative:
            if game_state.waiting_for_enemy_attack:
                self.render_waiting_message()
            else:
                self.render_hand(game_state.hand, game_state)
                # Renderizar botón de pasar turno si es posible
                self.render_pass_turn_button(game_state)
        
        # Renderizar narrativa
        if game_state.show_narrative:
            self.render_narrative(game_state.narrative_text)
        
        # Renderizar fin de juego
        if game_state.game_over:
            self.render_game_over(game_state.victory)
