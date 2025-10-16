import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self,sound_wall):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Check top/bottom collisions
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            pygame.mixer.Sound.play(sound_wall)  # Play wall sound

    def check_collision(self, player, ai, sound_paddle):
        ball_rect = self.rect()

        if ball_rect.colliderect(player.rect()) and self.velocity_x < 0:
            self.velocity_x *= -1
            self.x = player.x + player.width
            pygame.mixer.Sound.play(sound_paddle)

        if ball_rect.colliderect(ai.rect()) and self.velocity_x > 0:
            self.velocity_x *= -1
            self.x = ai.x - self.width
            pygame.mixer.Sound.play(sound_paddle)

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
