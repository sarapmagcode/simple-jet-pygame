# Simple Jet Game

A 2D arcade-style game built with Python and pygame. Fly your jet through the skies, avoid incoming missiles, and dodge clouds!

## Overview

This project was created to learn the fundamentals of pygame by building a complete 2D game. It features sprite-based rendering, collision detection, sound effects, and background music.

## Features

- Player-controlled jet with smooth movement
- Randomly spawning enemies (missiles) that fly toward the player
- Atmospheric clouds scrolling in the background
- Sound effects for movement and collisions
- Background music loop

## Requirements

- Python 3.x
- pygame library

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Install pygame:
```bash
pip install pygame
```

3. Run the game:
```bash
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys | Move the jet |
| W/A/S/D | Move the jet (alternative) |
| ESC | Quit game |

## How to Play

- Your jet starts in the center of the screen
- Missiles will spawn from the right and fly left
- Avoid colliding with missiles - the game ends on collision
- Clouds are harmless background elements

## Project Structure

```
simple-jet-pygame/
├── main.py              # Main game file
├── jet.png              # Player sprite (70x25 pixels)
├── missile.png          # Enemy sprite
├── cloud.png            # Background cloud sprite
├── Apoxode_-_Electric_1.mp3   # Background music
├── Rising_putter.ogg    # Upward movement sound
├── Falling_putter.ogg  # Downward movement sound
├── Collision.ogg       # Collision sound effect
├── README.md            # Project documentation
└── AGENTS.md            # Developer guidelines
```

## Learning Resources

- [Real Python pygame Primer](https://realpython.com/pygame-a-primer/) - The tutorial this project was based on
- [pygame Documentation](https://www.pygame.org/docs/) - Official pygame reference

## Credits

- Game tutorial: Real Python
- Background music: Apoxode - "Electric 1"
- Sound effects: OpenGameArt.org

## License

This project is for educational purposes. All assets are used under their respective licenses.
