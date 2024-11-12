import pygame
import sys
from player import Player
from const import *
from screen import Screen
# 初始化 pygame
pygame.init()

# 設定遊戲畫面
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2D Battle Game - Player vs Player')
scrn= Screen(WIDTH, HEIGHT)
# 顏色設置
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# BLUE = (0, 0, 255)
# BLACK = (0, 0, 0)
# GREEN = (0, 255, 0)
# YELLOW = (255, 255, 0)

# FPS 設置
#
# clock = pygame.time.Clock()

# 遊戲變數
# player1_health = 100
# player2_health = 100
player1_x, player1_y = 100, HEIGHT - 120
player2_x, player2_y = WIDTH - 160, HEIGHT - 120

# 設定遊戲的增減速度
# HEALTH_CHANGE_SPEED = 2
# ENERGY_CHANGE_SPEED = 1

# 重力與跳躍設定
# GRAVITY = 0.5
# JUMP_STRENGTH = -13
# MAX_FALL_SPEED = 20

# 攻擊冷卻時間設置（秒）
# ATTACK_COOLDOWN = 0.5
# player1_attack_time = 0
# player2_attack_time = 0
# attack_range = 100
# energy_gain_per_move = 0.5
# energy_full = 100


        
# 初始化玩家
player1 = Player(RED, player1_x, player1_y)
player2 = Player(BLUE, player2_x, player2_y)
scrn.addPlayer(player1, player2)
# all_sprites = pygame.sprite.Group()
# all_sprites.add(player1)
# all_sprites.add(player2)



# 主遊戲迴圈
def main_game():
    running = True
    map_choice = scrn.choose_map()
    countdown_time = 180  # Initialize countdown time once outside the loop
    font = pygame.font.SysFont('Arial', 24)
    # 載入背景圖像
    background_image = pygame.image.load(f'images/background/{map_choice}')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player1.update()
        player2.update()
        
        # 更新倒數計時
        countdown_time -= 1 / FPS
        if countdown_time <= 0:
            countdown_time = 0  # Stop the countdown at 0
        minutes = int(countdown_time // 60)
        seconds = int(countdown_time % 60)
        countdown_text = font.render(f'Time: {minutes:02}:{seconds:02}', True, YELLOW)
        
        
        # 玩家攻擊判斷
        current_time = pygame.time.get_ticks() / 1000
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            player1.attack(player2, current_time)
        if keys[pygame.K_SLASH]:
            player2.attack(player1, current_time)

        # 強力攻擊
        if keys[pygame.K_g] and player1.energy >= ENERGY_FULL:
            player1.attack(player2, current_time, powerful=True)
            player1.energy = 0
        if keys[pygame.K_PERIOD] and player2.energy >= ENERGY_FULL:
            player2.attack(player1, current_time, powerful=True)
            player2.energy = 0

        # Blit background image
        scrn.screen.blit(background_image, (0, 0))
        scrn.all_sprites.draw(scrn.screen)

        # 顯示玩家血量, 能量條, 倒數計時
        scrn.draw_health_energy_bar()
        scrn.screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, 20))
        
        # 檢查遊戲結束
        if player1.health <= 0 or player2.health <= 0:
            winner = "Player 1" if player2.health <= 0 else "Player 2"
            scrn.show_game_over(winner)
            if keys[pygame.K_r]:
                player1.health = player2.health = 100
                player1.energy = player2.energy = 0
                player1.rect.x = player1_x
                player1.rect.y = HEIGHT - 120
                player2.rect.x = player2_x
                player2.rect.y = HEIGHT - 120
            elif keys[pygame.K_q]:
                running = False
        
        pygame.display.update()
        scrn.clock.tick(FPS)
    pygame.quit()
    sys.exit()

def menu_loop():
    menu_running = True
    while menu_running:
        scrn.show_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Start Game
                if HEIGHT // 2 <= mouse_y <= HEIGHT // 2 + 40 and WIDTH // 2 - 150 <= mouse_x <= WIDTH // 2 + 150:
                    menu_running = False
                    main_game()
                # Quit Game
                if HEIGHT // 2 + 60 <= mouse_y <= HEIGHT // 2 + 100 and WIDTH // 2 - 100 <= mouse_x <= WIDTH // 2 + 100:
                    menu_running = False
                    pygame.quit()
                    sys.exit()

menu_loop()