import pygame
from .paddle import Paddle
from .ball import Ball
import random


pygame.init()
pygame.mixer.init()  # Initialize mixer for sounds


# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.winning_score = 5

        self.sound_paddle = pygame.mixer.Sound("sounds/paddle_hit.mp3")
        self.sound_wall = pygame.mixer.Sound("sounds/wall_bounce.mp3")
        self.sound_score = pygame.mixer.Sound("sounds/score.mp3")

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)


        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move(self.sound_wall)
        self.ball.check_collision(self.player, self.ai, self.sound_paddle)
        
        if self.ball.x <= 0:
            self.ai_score += 1
            pygame.mixer.Sound.play(self.sound_score)
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            pygame.mixer.Sound.play(self.sound_score)
            self.ball.reset()
    
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

   
    def check_game_over(self):
        screen = pygame.display.get_surface()
        
        # Check if anyone has won
        if self.player_score >= self.winning_score:
            message = "Player Wins!"
        elif self.ai_score >= self.winning_score:
            message = "AI Wins!"
        else:
            return None  # Game continues

        # Stop ball movement
        self.ball.velocity_x = 0
        self.ball.velocity_y = 0

        # Display game over message
        screen.fill((0, 0, 0))
        text = self.font.render(message, True, (255, 255, 255))
        rect = text.get_rect(center=(self.width // 2, self.height // 2))
        screen.blit(text, rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Show message for 2 seconds

        # Show replay options
        replay = self.show_replay_options()  # Returns True if replay selected, False if exit
        return replay

    def reset_match(self):
        # Reset scores
        self.player_score = 0
        self.ai_score = 0

        # Reset ball position and velocity
        self.ball.reset()
        

        # Reset paddles to vertical center
        self.player.y = self.height // 2 - self.player.height // 2
        self.ai.y = self.height // 2 - self.ai.height // 2


    def show_replay_options(self):
        screen = pygame.display.get_surface()
        font = pygame.font.SysFont("Arial", 28)
        options_text = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]

        selecting = True
        series_total_matches = 1  # Default first match already played
        while selecting:
            screen.fill((0, 0, 0))
            for i, line in enumerate(options_text):
                text = font.render(line, True, (255, 255, 255))
                rect = text.get_rect(center=(self.width // 2, self.height // 2 - 60 + i*40))
                screen.blit(text, rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False  # Exit game
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        series_total_matches = 3
                        selecting = False
                    elif event.key == pygame.K_5:
                        series_total_matches = 5
                        selecting = False
                    elif event.key == pygame.K_7:
                        series_total_matches = 7
                        selecting = False
                    elif event.key == pygame.K_ESCAPE:
                        return False  # Exit game

        # Series tracking
        series_results = []
        series_results.append("Player" if self.player_score >= self.winning_score else "AI")

        # Play remaining matches
        for match in range(1, series_total_matches):
    
            self.reset_match()   


            match_over = False
            while not match_over:
                # Game loop for this match
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                self.handle_input()
                self.update()
                self.render(screen)
                pygame.display.flip()
                pygame.time.delay(16)  # ~60 FPS

                # Check if match is over
                if self.player_score >= self.winning_score:
                    series_results.append("Player")
                    match_over = True
                elif self.ai_score >= self.winning_score:
                    series_results.append("AI")
                    match_over = True

        # Determine overall winner
        player_wins = series_results.count("Player")
        ai_wins = series_results.count("AI")

        screen.fill((0, 0, 0))
        if player_wins > ai_wins:
            message = f"Player wins the series {player_wins}-{ai_wins}"
        else:
            message = f"AI wins the series {ai_wins}-{player_wins}"
        
        text = self.font.render(message, True, (255, 255, 255))
        rect = text.get_rect(center=(self.width // 2, self.height // 2))
        screen.blit(text, rect)
        pygame.display.flip()
        pygame.time.delay(3000)  # Show series winner

        return True
    #New3