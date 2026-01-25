# Crisis Planetaria: Tecnología al Rescate

Un juego de cartas roguelike educativo estilo "Slay the Spire" desarrollado en Python con Pygame, preparado para entorno web mediante Pygbag.

## Contexto del Proyecto

Este juego es una demo para un proyecto intermodular sobre:
- **Biotecnología**: Soluciones verdes y sostenibles
- **Computación Cuántica**: Procesamiento de datos y algoritmos avanzados
- **Exploración Espacial**: Tecnologías para resolver crisis globales

El juego se desarrolla en un contexto temporal entre 2020 y 2040, enfrentando crisis climáticas y de salud.

## Características del Juego

### Sistema de Turnos
- **Energía Base**: 3 puntos por turno
- **Carta Especial**: "Q-Bit Extra" que aumenta +1 energía
- **Fin de Turno**: Cuando la energía llega a 0, el jugador debe hacer clic para que el enemigo ataque
- **Renovación**: Después del ataque, se renueva la mano (3 cartas nuevas) y se resetea la energía

### Sistema de Enemigos
Tres mini-jefes progresivos:
1. **Residuos Plásticos** (50 HP, 8 daño)
2. **Lobby Negacionista** (75 HP, 12 daño)
3. **Crisis Energética** (100 HP, 15 daño)

Cada enemigo tiene:
- Representación visual en arte ASCII
- Narrativa educativa al ser derrotado explicando cómo la tecnología resolvió la crisis

### Condiciones de Victoria/Derrota
- **Derrota**: Si el HP del "Planeta" llega a 0
- **Victoria**: Derrotar a los 3 enemigos
- Sistema de reintento disponible

### Estética Deep Tech
- **Fondo**: Casi negro (5, 5, 10)
- **Biotecnología**: Verde esmeralda (0, 255, 127)
- **Cuántica**: Cian neón (0, 255, 255)
- **Espacio**: Violeta/Púrpura (138, 43, 226)

## Instalación

### Requisitos
- Python 3.8 o superior
- Pygame 2.5.0 o superior

### Instalación Local
```bash
pip install -r requirements.txt
python main.py
```

### Preparación para Web (Pygbag)
```bash
pip install pygbag
pygbag main.py
```

## Estructura del Proyecto

```
.
├── main.py          # Bucle principal con asyncio para Pygbag
├── game.py          # Lógica del juego (estado, turnos, combate)
├── cards.py         # Sistema de cartas y efectos
├── enemies.py       # Definición de enemigos y narrativas
├── ui.py            # Interfaz de usuario y renderizado
├── requirements.txt # Dependencias
└── README.md        # Este archivo
```

## Controles

- **Clic Izquierdo**: Jugar carta o interactuar con botones
- **ESC**: Salir del juego

## Características Técnicas

### Seguridad Anti-Crash
- Validaciones en todos los índices de arrays
- Manejo de excepciones en operaciones críticas
- Verificaciones de existencia de objetos antes de acceso
- `await asyncio.sleep(0)` en el bucle principal para compatibilidad con Pygbag

### Sistema de Cartas
Las cartas muestran:
- **Nombre**: Identificación de la carta
- **Coste**: Energía requerida
- **Tipo**: Biotecnología, Cuántica o Espacial
- **Descripción**: Efecto de la carta

## Desarrollo

Este proyecto fue desarrollado como demo educativa para demostrar cómo las tecnologías emergentes pueden resolver crisis globales a través de un formato de juego interactivo.

## Licencia

Proyecto educativo - Uso libre para fines educativos.
