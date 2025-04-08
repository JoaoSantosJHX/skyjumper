import random
from pygame import Rect

WIDTH = 1024
HEIGHT = 512
GROUND_Y = 420

game_started = False
show_music_toggle = True
music_on = True
game_over = False
hovered_button = None
score = 0

# Botões
buttons = {
    "start": Rect(WIDTH//2 - 100, 200, 200, 50),
    "toggle_music": Rect(WIDTH//2 - 100, 270, 200, 50),
    "exit": Rect(WIDTH//2 - 100, 340, 200, 50),
    "menu": Rect(WIDTH//2 - 100, 300, 200, 50)
}

# Lista de imagens dos obstáculos
obstacle_images = ['obstaculo', 'obstaculo2', 'obstaculo3', 'obstaculo4']


def play_music(track_name):
    if music_on:
        music.stop()
        music.play(track_name)
    else:
        music.stop()

def init_game():
    global hero, obstacle, gravity, jump_force, on_ground, game_over, score

    hero = Actor('player_idle')
    hero.x = 100
    hero.y = GROUND_Y - hero.height // 2
    hero.vy = 0
    gravity = 1
    jump_force = -18
    on_ground = True

    obstacle = Actor(random.choice(obstacle_images))
    obstacle.x = WIDTH + 200
    obstacle.y = GROUND_Y - obstacle.height // 2

    score = 0
    game_over = False

init_game()

def draw_button(rect, text, color, hover=False):
    border_color = "white" if not hover else "yellow"
    screen.draw.filled_rect(rect, color)
    screen.draw.rect(rect, border_color)
    screen.draw.text(text, center=rect.center, color="white")

def draw():
    screen.clear()

    if not game_started:
        screen.blit('plataforma', (0, 0))
        screen.draw.text("Sky Jumper", center=(WIDTH//2, 100), fontsize=60, color="white")

        draw_button(buttons["start"], "Jogar", "blue", hovered_button == "start")
        draw_button(buttons["toggle_music"], f"Musica: {'ON' if music_on else 'OFF'}", "green", hovered_button == "toggle_music")
        draw_button(buttons["exit"], "Sair", "red", hovered_button == "exit")

    elif game_over:
        screen.blit('plataforma', (0, 0))
        screen.draw.text("Game Over", center=(WIDTH//2, 180), fontsize=60, color="red")
        screen.draw.text(f"Pontos: {score}", center=(WIDTH//2, 240), fontsize=40, color="white")

        draw_button(buttons["menu"], "Voltar ao Menu", "orange", hovered_button == "menu")

    else:
        screen.blit('plataforma', (0, 0))
        screen.draw.filled_rect(Rect(0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y), 'green')

        hero.draw()
        obstacle.draw()

        screen.draw.text(f"Pontos: {score}", topleft=(20, 20), fontsize=35, color="white")

def update():
    global on_ground, game_over, score

    if not game_started or game_over:
        return

    hero.vy += gravity
    hero.y += hero.vy

    if hero.y >= GROUND_Y - hero.height // 2:
        hero.y = GROUND_Y - hero.height // 2
        hero.vy = 0
        on_ground = True
    else:
        on_ground = False

    obstacle.x -= 6
    if obstacle.right < 0:
        obstacle.x = WIDTH + random.randint(100, 300)
        obstacle.image = random.choice(obstacle_images)
        score += 1

    if hero.colliderect(obstacle):
        print("Game Over")
        game_over = True
        music.stop()
        sounds.hit.play()

def on_key_down(key):
    if key == keys.SPACE and on_ground and not game_over:
        hero.vy = jump_force
        sounds.jump.play()

def on_mouse_down(pos):
    global game_started, music_on

    for name, rect in buttons.items():
        if rect.collidepoint(pos):
            sounds.click.play()

    if not game_started:
        if buttons["start"].collidepoint(pos):
            game_started = True
            play_music('playingsong')
            init_game()
        elif buttons["toggle_music"].collidepoint(pos):
            music_on = not music_on
            if music_on:
                play_music('menusong' if not game_started else 'playingsong')
            else:
                music.stop()
        elif buttons["exit"].collidepoint(pos):
            exit()
    elif game_over:
        if buttons["menu"].collidepoint(pos):
            game_started = False
            play_music('menusong')

def on_mouse_move(pos):
    global hovered_button
    hovered_button = None
    for name, rect in buttons.items():
        if rect.collidepoint(pos):
            hovered_button = name
            break
