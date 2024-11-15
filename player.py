import pygame
from ch import character
from const import *
class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y, index):
        super().__init__()
        # Model
        self.color = color
        self.image = pygame.image.load(character.character_data[index]['icon']) if color == RED else pygame.image.load(character.character_data[index]['icon'])
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Status
        self.health = 100
        self.energy = 0
        self.displayed_health = 100
        self.displayed_energy = 0
        self.defending = False
        self.y_velocity = 0
        self.jumping = False
        self.last_jump_time = 0 
        self.jump_count = 0
        self.facing_left = False
        self.attack_time = 0
        # Attributes
        self.attack_damage = 10
        self.attack_damage_powerful = 30
        self.energy_gain_per_move = 0.5
        self.velocity = 5
        self.attack_range = 100
        self.defend_strength = 20
        
        self.k_left = pygame.K_a if color == RED else pygame.K_LEFT
        self.k_right = pygame.K_d if color == RED else pygame.K_RIGHT
        self.k_up = pygame.K_w if color == RED else pygame.K_UP
        self.k_down = pygame.K_s if color == RED else pygame.K_DOWN
        
    def update(self):
        # 使顯示的血量和能量逐漸逼近實際值
        health_change_speed = 1  # 控制血量變化速度
        energy_change_speed = 3  # 控制能量變化速度

        if self.displayed_health < self.health:
            self.displayed_health += health_change_speed
            if self.displayed_health > self.health:
                self.displayed_health = self.health
        elif self.displayed_health > self.health:
            self.displayed_health -= health_change_speed
            if self.displayed_health < self.health:
                self.displayed_health = self.health

        if self.displayed_energy < self.energy:
            self.displayed_energy += energy_change_speed
            if self.displayed_energy > self.energy:
                self.displayed_energy = self.energy
        elif self.displayed_energy > self.energy:
            self.displayed_energy -= energy_change_speed
            if self.displayed_energy < self.energy:
                self.displayed_energy = self.energy
        
        # 移動控制和能量增加
        keys = pygame.key.get_pressed()
        moved = False
        self.defending = False
        if keys[self.k_left]:
            self.rect.x -= self.velocity
            moved = True
            if not self.facing_left:  # Only flip if direction has changed
                self.facing_left = True
                self.image = pygame.transform.flip(self.image, True, False)  # Flip horizontally
        if keys[self.k_right]:
            self.rect.x += self.velocity
            moved = True
            if self.facing_left:  # Only flip if direction has changed
                self.facing_left = False
                self.image = self.image
                self.image = pygame.transform.flip(self.image, True, False)
            # Jump logic with 0.5 second delay after last jump
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        if keys[self.k_up] and self.jump_count < 2 and current_time - self.last_jump_time > 400:
            self.y_velocity = JUMP_STRENGTH
            self.jumping = True
            self.jump_count += 1
            self.last_jump_time = current_time  # Update last jump time
        # If you're in the air and press down, you will fall faster
        if keys[self.k_down] and self.jumping:
            self.y_velocity = MAX_FALL_SPEED
        elif keys[self.k_down]:
            self.defending = True

        # 更新能量
        if moved:
            self.energy += self.energy_gain_per_move
            if self.energy > ENERGY_FULL:
                self.energy = ENERGY_FULL

        # Gravity
        if self.jumping:
            self.y_velocity += GRAVITY
            if self.y_velocity > MAX_FALL_SPEED:
                self.y_velocity = MAX_FALL_SPEED

        self.rect.y += self.y_velocity

        # Check if landed
        if self.rect.y >= HEIGHT - 220:
            self.rect.y = HEIGHT - 220
            self.jumping = False
            self.y_velocity = 0
            self.jump_count = 0  # Reset jump count when the player lands
            
    def attack(self, other_player, current_time, powerful=False):
        # global player1_attack_time, player2_attack_time

        # if self.color == RED and current_time - self.attack_time > ATTACK_COOLDOWN: # player1_attack_time >= ATTACK_COOLDOWN:
        if(current_time - self.attack_time > ATTACK_COOLDOWN):
            #player1_attack_time = current_time
            self.attack_time = current_time
            if abs(self.rect.x - other_player.rect.x) < self.attack_range:
                damage = self.attack_damage_powerful if powerful else self.attack_damage
                if other_player.defending:
                    damage -= other_player.defend_strength
                    if damage < 0:
                        damage = 0
                other_player.health -= damage

    def draw(self, screen):
        # Draw player image on screen
        screen.blit(self.image, self.rect)