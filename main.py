# Refer to https://realpython.com/pygame-a-primer/
import pygame
from pygame.locals import (
  RLEACCEL,
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_ESCAPE,
  KEYDOWN,
  K_w,
  K_a,
  K_s,
  K_d,
  QUIT
)
import random

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# "Sprite" - a 2d representation of something on the screen
# (basically, a picture)
class Player(pygame.sprite.Sprite):
  def __init__(self):
    super(Player, self).__init__()
    # self.surf = pygame.Surface((75, 25))
    # self.surf.fill((255, 255, 255))
    
    # convert() - optimizes the Surface, making future blit() calls faster
    self.surf = pygame.image.load("jet.png").convert()
    
    # set_colorkey() - indicates the color pygame will render a transparent (in our
    # case, it is white).
    # RLEACCEL - helps pygame render more quickly on non-accelerated displays (optional).
    self.surf.set_colorkey((255, 255, 255), RLEACCEL)

    self.rect = self.surf.get_rect()

  def update(self, pressed_keys):
    """
    Move the sprite based on the user keypresses

    :param self: Player attributes
    :param pressed_keys: Currently held down keys
    """
    if pressed_keys[K_UP] or pressed_keys[K_w]:
      self.rect.move_ip(0, -5) # move_ip() stands for move in place
      move_up_sound.play()

    if pressed_keys[K_DOWN] or pressed_keys[K_s]:
      self.rect.move_ip(0, 5)
      move_down_sound.play()

    if pressed_keys[K_LEFT] or pressed_keys[K_a]:
      self.rect.move_ip(-5, 0)

    if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
      self.rect.move_ip(5, 0)

    # Keep player on the screen
    if self.rect.left < 0:
      self.rect.left = 0

    if self.rect.right > SCREEN_WIDTH:
      self.rect.right = SCREEN_HEIGHT

    if self.rect.top <= 0:
      self.rect.top = 0

    if self.rect.bottom >= SCREEN_HEIGHT:
      self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
  def __init__(self):
    super(Enemy, self).__init__()
    # self.surf = pygame.Surface((20, 10))
    # self.surf.fill((255, 255, 255))

    self.surf = pygame.image.load("missile.png").convert()
    self.surf.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.surf.get_rect(
      center=(
        random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
        random.randint(0, SCREEN_HEIGHT)
      )
    )
    self.speed = random.randint(5, 20)

  def update(self):
    self.rect.move_ip(-self.speed, 0)
    # Remove the sprite when it passes the left edge of the screen
    if self.rect.right < 0:
      # Sprite is removed from every Group to which it belongs (Sprite Groups)
      # Python's garbage collector reclaims the memory as necessary
      self.kill()


class Cloud(pygame.sprite.Sprite):
  def __init__(self):
    """
    Initialize Surface and Rect
    
    :param self: User-defined attributes
    """
    super(Cloud, self).__init__()
    self.surf = pygame.image.load("cloud.png").convert()
    self.surf.set_colorkey((0, 0, 0), RLEACCEL)
    self.rect = self.surf.get_rect(
      center=(
        random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
        random.randint(0, SCREEN_HEIGHT)
      )
    )
  
  def update(self):
    self.rect.move_ip(-5, 0) # Toward the left side (constant speed)
    if self.rect.right < 0:
      self.kill()


# Setup for sounds. Defaults are good.
pygame.mixer.init()

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock() # Setup clock for a decent frame rate

# Create a custom event for adding a new enemy.
# Pygame defines events internally as integers.
# USEREVENT - last event pygame reserves (to ensure your custom event is unique).
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250) # Fires it every 250ms
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000) # Fires it every 1s

player = Player()

# Create groups to hold sprites:
# enemies - used for collision detection and position updates
# clouds - used for position updates
# all_sprites - used for rendering
# We created multiple groups so that we can change the way sprite move
# or behave without impacting the movement or behavior of other sprites
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Load and play background music
pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1) # -1 means never end

# Load all sound files
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

# Set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)

running = True

# Every cycle of the game loop is called a "frame", and the quicker
# you can do things each cycle, the faster your game will run
while running:
  # All events in pygame are placed in the event queue, which can be
  # accessed and manipulated (event-handling loop)
  for event in pygame.event.get():
    if event.type == KEYDOWN and event.key == K_ESCAPE:
        running = False
    elif event.type == QUIT:
      running = False
    elif event.type == ADDENEMY: # Add a new enemy?
      new_enemy = Enemy()
      enemies.add(new_enemy)
      all_sprites.add(new_enemy)
    elif event.type == ADDCLOUD: # Add a new cloud?
      new_cloud = Cloud()
      clouds.add(new_cloud)
      all_sprites.add(new_cloud)

  # Updates the position of enemies and clouds
  enemies.update()
  clouds.update()

  pressed_keys = pygame.key.get_pressed() # Returns a dictionary
  player.update(pressed_keys)

  screen.fill((135, 206, 250))

  # Anything put into all_sprites will be drawn with every frame.
  for entity in all_sprites:
    # "Surface" is a rectangular object on which you can draw.
    # "blit" (Block Transfer) - Copy the contents of one Surface to another.
    # If you pass a "Rect" to blit(source, dest), it uses the coordinates of the 
    # top-left corner.
    screen.blit(entity.surf, entity.rect)
  
  # spritecollideany(sprite, group)
  # - Check if the Player (sprite) collides with one of enemies (group)
  if pygame.sprite.spritecollideany(player, enemies):
    player.kill()

    # Stop any moving sounds and play the collision sound
    move_up_sound.stop()
    move_down_sound.stop()
    collision_sound.play()
    
    running = False
  
  # Updates the entire screen with everything that's been drawn 
  # since the last flip
  pygame.display.flip()

  # Ensure program maintains a rate of 30 frames per second
  clock.tick(30)

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
