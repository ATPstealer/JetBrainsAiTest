import random

import pygame
from pygame.math import Vector2
import time

pygame.init()
pygame.font.init()


class Ball:
    def __init__(self, pos, vel, acc):
        self.pos = Vector2(pos)
        self.vel = Vector2(random.uniform(-0.04, 0.04), random.uniform(-0.04, 0.04))
        self.acc = Vector2(acc)

    def update_position(self, gravity):
        self.pos += self.vel
        if gravity:
            self.vel += self.acc


class Wall:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)


class GameScreen:
    def __init__(self, width, height):
        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.SysFont(None, 30)
        self.start_time = time.time()

    def render_game(self, ball, walls, active_wall):
        self.screen.fill((0, 0, 0))
        pygame.draw.circle(self.screen, (255, 255, 255), ball.pos, 20)
        for i, wall in enumerate(walls):
            color = (0, 0, 255) if i == active_wall else (255, 0, 0)
            pygame.draw.rect(self.screen, color, wall.rect)
        elapsed_time = time.time() - self.start_time
        time_text = self.font.render(f'Time: {int(elapsed_time)}', False, (255, 255, 255))
        self.screen.blit(time_text, (10, 10))
        pygame.display.update()


def handle_gravity(ball, walls, mouse_pos):
    for i, wall in enumerate(walls):
        if wall.rect.collidepoint(mouse_pos):
            ball.acc = Vector2(0, 0.1 if i == 3 else -0.1) * 0.0001 if i == 0 or i == 3 \
                else Vector2(0.1 if i == 2 else -0.1, 0) * 0.0001
            return i
    return None


def main():
    ball = Ball((400, 300), (0, 0), (0, 0))
    walls = [Wall(50, 50, 700, 10), Wall(50, 50, 10, 500),
             Wall(740, 50, 10, 500), Wall(50, 540, 700, 10)]
    screen = GameScreen(800, 600)
    gravity = False
    active_wall = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = Vector2(pygame.mouse.get_pos())
                gravity = not gravity
                if gravity:
                    active_wall = handle_gravity(ball, walls, mouse_pos)
                else:
                    ball.acc = Vector2(0, 0)
                    active_wall = None
        ball.update_position(gravity)
        if any(wall.rect.collidepoint(ball.pos) for wall in walls):
            print("Game Over")
            running = False
        screen.render_game(ball, walls, active_wall)
    pygame.quit()


if __name__ == "__main__":
    main()