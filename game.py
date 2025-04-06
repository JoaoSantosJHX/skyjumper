import pgzrun
import pygame
from random import randint
from pgzero.actor import Actor

# tamanho da janela
WIDTH = 800
HEIGHT = 600

# Estados do jogo
game_state = "menu" # Pode ser "menu", "playing" ou "game_over"

# Controle de som
sound_on = True

# --- Botões do menu ---
class Button:
    def __init__(self, text, pos, action):
        self.text = text
        self.pos = pos
        self.action = action
        self.width = 200
        self.height = 50

    
    def draw(self):
        screen.draw.filled_rect(Rect((self.pos[0], self.pos[1]), (self.width, self.height)), "darkblue")
        screen.draw.text(self.text, center=(self.pos[0] + self.width//2, self.pos[1] + self.height//2), fontsize=32, color="white")


    def is_clicked(self, mouse_pos):
        rect = Rect((self.pos[0], self.pos[1]), (self.width, self.height))
        return rect.collidepoint(mouse_pos)  


# criação dos botões
buttons = [
    Button("Start Game", (300,150), "start"),
    Button("Sound: On", (300,220), "toggle_sound"),
    Button("Exit", (300,290), "exit")
]                

# Botões dentro do estado "playing"
pause_play_button = Button("Pause", (10, 10), "toggle_pause")
back_to_menu_button = Button("Menu", (10, 70), "back_to_menu")


# --- Jogador ---
player = Actor("player_idle")
player._surf = pygame.transform.scale(player._surf, (60, 60))  # Ajuste o tamanho conforme necessário
player.width = 60
player.height = 60
player.x = WIDTH // 2
player.y = HEIGHT - 150


# Física do jogador
player.vy = 0 # velocidade vertical
player.vx = 0  # Velocidade horizontal
gravity = 0.5 # gravidade
jump_strength = -10 # força do pulo
move_speed = 5 # velocidade de movimento
is_jumping = False # controle de pulo

# Função para desenhar
def draw():
    print("🔄 draw() foi chamado")
    screen.clear()

    if game_state == "menu":
        screen.draw.text("Sky Jumper", center=(WIDTH//2, 80), fontsize=60, color="orange")
        for btn in buttons:
            btn.draw()

    elif game_state in ["playing", "paused"]:
        for obstaculo in obstaculos:
            obstaculo.draw()
        for plataforma in plataformas:
            plataforma.draw()
        player.draw()

        # Botões de pause/menu
        pause_play_button.draw()
        back_to_menu_button.draw()

        if game_state == "paused":
            screen.draw.text("Jogo Pausado", center=(WIDTH//2, HEIGHT//2), fontsize=50, color="yellow")

    elif game_state == "game_over":
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=80, color="red")
        screen.draw.text("Clique para voltar ao menu", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=30, color="white")

          


# Função para cliques do mouse
def on_mouse_down(pos):
    global game_state, sound_on

    if game_state == "menu":
        for btn in buttons:
            if btn.is_clicked(pos):
                if btn.action == "start":
                    game_state = "playing"
                elif btn.action == "toggle_sound":
                    sound_on = not sound_on
                    btn.text = f"Sound: {'On' if sound_on else 'Off'}"
                elif btn.action == "exit":
                    exit()

    elif game_state in ["playing", "paused"]:
        if pause_play_button.is_clicked(pos):
            game_state = "paused" if game_state == "playing" else "playing"
            pause_play_button.text = "Play" if game_state == "paused" else "Pause"

        elif back_to_menu_button.is_clicked(pos):
            game_state = "menu"
    
    elif game_state == "game_over":
        game_state = "menu"


# detecção de tecla para pular
def on_key_down(key):
    global is_jumping
    if key == keys.SPACE and not is_jumping:
        player.vy = jump_strength
        is_jumping = True

# Função update
def update():
    global game_state
    global is_jumping

    if game_state != "playing":
        
        return #pausa o jogo
    
    for obstaculo in obstaculos:
        obstaculo.update()

        if obstaculo.colide_com(player):
            print("🔥 Colidiu com obstáculo!")
            game_state = "game_over"

    # movimento lateral
    player.vx = 0
    if keyboard.left:
        player.vx = -move_speed
    elif keyboard.right:
        player.vx = move_speed

    # Aplica movimento horizontal
    player.x += player.vx

    # Limites laterais
    if player.x < 0:
        player.x = 0
    elif player.x > WIDTH:
        player.x = WIDTH

    # Aplica gravidade
    player.vy += gravity
    player.y += player.vy  # ⬅ Aqui você aplica o movimento vertical

    # Verifica colisão com plataformas
    on_plataforma = False
    for plataforma in plataformas:
        if (player.colliderect(plataforma.actor) and
            player.vy >= 0 and
            player.y < plataforma.actor.y):
            player.y = plataforma.actor.y - player.height / 2
            player.vy = 0
            is_jumping = False
            on_plataforma = True
            break

    # Chão (caso não esteja em plataforma)
    if not on_plataforma and player.y >= HEIGHT - 100:
        player.y = HEIGHT - 100
        player.vy = 0
        is_jumping = False


# --- Plataforma ---
class Plataforma:
    def __init__(self, x, y):
        self.actor = Actor("plataforma")
        self.actor.pos = (x, y)

    def draw(self):
        self.actor.draw()

    def colide_com(self, jogador):
        return self.actor.colliderect(jogador)
    
# Lista de plataformas
plataformas = [
    Plataforma(300, 450),
    Plataforma(150, 350),
    Plataforma(500, 250)
]

# --- Obstáculo ---
class Obstaculo:
    def __init__(self, x, y):
        self.actor = Actor("obstaculo")  # imagem: images/obstaculo.png
        self.actor.pos = (x, y)
        self.speed = 2  # velocidade de movimento horizontal

    def draw(self):
        self.actor.draw()

    def update(self):
        # Movimento lateral (opcional)
        self.actor.x += self.speed
        if self.actor.left < 0 or self.actor.right > WIDTH:
            self.speed *= -1  # inverte a direção

    def colide_com(self, jogador):
        return self.actor.colliderect(jogador)
    
# Lista de obstáculos
obstaculos = [
    Obstaculo(200, 400),
    Obstaculo(600, 300)
]

pgzrun.go()
    